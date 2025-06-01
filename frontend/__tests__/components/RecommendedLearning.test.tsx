import '@testing-library/jest-native/extend-expect';
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import React from 'react';
import { render, waitFor, fireEvent } from '@testing-library/react-native';

jest.mock('../../src/utils/api', () => {
  const mockApi = {
    learning: { getAll: jest.fn() },
  };
  return {
    __esModule: true,
    api: mockApi,
    default: mockApi,
  };
});

import RecommendedLearning from '../../src/components/RecommendedLearning';
import { api } from '../../src/utils/api';

describe('RecommendedLearning', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state initially', () => {
    const { getByTestId } = render(<RecommendedLearning onPress={() => {}} />);
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });

  it('renders learning items after loading', async () => {
    const mockData = {
      items: [
        { id: '1', title: 'Test Item 1', shortDescription: 'Desc 1', difficulty: 'advanced' },
        { id: '2', title: 'Test Item 2', shortDescription: 'Desc 2', difficulty: 'advanced' },
      ],
    };
    (api.learning.getAll as any).mockResolvedValue(mockData);
    const { getByText, getAllByTestId } = render(<RecommendedLearning onPress={() => {}} />);
    await waitFor(() => {
      expect(getByText('Test Item 1')).toBeTruthy();
      expect(getByText('Desc 1')).toBeTruthy();
      expect(getByText('Test Item 2')).toBeTruthy();
      expect(getByText('Desc 2')).toBeTruthy();
    });
    // 检查 testID
    const items = getAllByTestId('learning-item');
    expect(items.length).toBe(2);
  });

  it('handles item press correctly', async () => {
    const mockData = {
      items: [
        { id: '1', title: 'Test Item 1', shortDescription: 'Desc 1', difficulty: 'advanced' },
      ],
    };
    (api.learning.getAll as any).mockResolvedValue(mockData);
    const mockOnPress = jest.fn();
    const { getAllByTestId } = render(<RecommendedLearning onPress={mockOnPress} />);
    await waitFor(() => {
      const items = getAllByTestId('learning-item');
      fireEvent.press(items[0]);
      expect(mockOnPress).toHaveBeenCalledWith(mockData.items[0]);
    });
  });

  it('displays error message when API call fails', async () => {
    (api.learning.getAll as any).mockRejectedValue(new Error('API Error'));
    const { getByText } = render(<RecommendedLearning onPress={() => {}} />);
    await waitFor(() => {
      expect(getByText('加载数据失败，请重试')).toBeTruthy();
    });
  });

  it('retries loading when retry button is pressed', async () => {
    const mockData = {
      items: [
        { id: '1', title: 'Test Item 1', shortDescription: 'Desc 1', difficulty: 'advanced' },
      ],
    };
    (api.learning.getAll as any)
      .mockRejectedValueOnce(new Error('API Error'))
      .mockResolvedValueOnce(mockData);
    const { getByText, getAllByTestId } = render(<RecommendedLearning onPress={() => {}} />);
    await waitFor(() => {
      expect(getByText('加载数据失败，请重试')).toBeTruthy();
    });
    const retryButton = getByText('重试');
    fireEvent.press(retryButton);
    await waitFor(() => {
      expect(getByText('Test Item 1')).toBeTruthy();
      expect(getByText('Desc 1')).toBeTruthy();
      const items = getAllByTestId('learning-item');
      expect(items.length).toBe(1);
    });
  });
}); 