import { describe, it, expect, jest } from '@jest/globals';
import React from 'react';
import { render } from '@testing-library/react-native';
import AppNavigator from '../../src/navigation/AppNavigator';

// Mock the screens and tab navigator
jest.mock('@react-navigation/bottom-tabs', () => {
  return {
    createBottomTabNavigator: () => ({
      Navigator: ({ children }) => children,
      Screen: ({ name }) => name,
    }),
  };
});

// Mock screens
jest.mock('../../src/screens/HomeScreen', () => 'HomeScreen');
jest.mock('../../src/screens/LearningScreen', () => 'LearningScreen');
jest.mock('../../src/screens/NewsScreen', () => 'NewsScreen');
jest.mock('../../src/screens/QuestionsScreen', () => 'QuestionsScreen');

describe('AppNavigator', () => {
  it('renders without crashing', () => {
    render(<AppNavigator />);
  });
  
  it('includes all required tabs', () => {
    const { toJSON } = render(<AppNavigator />);
    const tree = JSON.stringify(toJSON());
    expect(tree).toContain('HomeTab');
    expect(tree).toContain('LearningTab');
    expect(tree).toContain('NewsTab');
    expect(tree).toContain('QuestionsTab');
  });
}); 