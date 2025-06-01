import '@testing-library/jest-native/extend-expect';
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import React from 'react';
import { render, waitFor } from '@testing-library/react-native';

jest.mock('../../src/utils/api', () => {
  const mockApi = {
    learning: { getAll: jest.fn() },
    news: { getAll: jest.fn() },
    questions: { getAll: jest.fn() },
  };
  return {
    __esModule: true,
    api: mockApi,
    default: mockApi,
  };
});

import HomeScreen from '../../src/screens/HomeScreen';
import { api } from '../../src/utils/api';

// Mock navigation
jest.mock('@react-navigation/native', () => ({
  useNavigation: () => ({
    navigate: jest.fn(),
  }),
}));

describe('HomeScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state initially', () => {
    const { getByTestId } = render(<HomeScreen />);
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });

  it('renders content after loading', async () => {
    const mockData = {
      items: [
        { id: 1, title: 'Test Item 1' },
        { id: 2, title: 'Test Item 2' },
      ],
    };
    (api.learning.getAll as any).mockResolvedValue(mockData);
    (api.news.getAll as any).mockResolvedValue(mockData);
    (api.questions.getAll as any).mockResolvedValue(mockData);
    const { getByTestId } = render(<HomeScreen />);
    await waitFor(() => {
      expect(getByTestId('home-content')).toBeTruthy();
    });
  });

  it('renders all three main components when data loads', async () => {
    const mockData = {
      items: [
        { id: 1, title: 'Test Item 1' },
        { id: 2, title: 'Test Item 2' },
      ],
    };
    (api.learning.getAll as any).mockResolvedValue(mockData);
    (api.news.getAll as any).mockResolvedValue(mockData);
    (api.questions.getAll as any).mockResolvedValue(mockData);
    const { getByText } = render(<HomeScreen />);
    await waitFor(() => {
      expect(getByText('今日推荐学习')).toBeTruthy();
      expect(getByText('最新财经新闻')).toBeTruthy();
      expect(getByText('你可能感兴趣的问题')).toBeTruthy();
    });
  });

  it('displays error message when API call fails', async () => {
    (api.learning.getAll as any).mockRejectedValue(new Error('Failed to load data'));
    (api.news.getAll as any).mockRejectedValue(new Error('Failed to load data'));
    (api.questions.getAll as any).mockRejectedValue(new Error('Failed to load data'));
    const { getByText } = render(<HomeScreen />);
    await waitFor(() => {
      expect(getByText('加载数据失败，请重试')).toBeTruthy();
    });
  });
}); 