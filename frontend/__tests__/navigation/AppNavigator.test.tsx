import { describe, it, expect, jest } from '@jest/globals';
import React from 'react';
import { render } from '@testing-library/react-native';
import AppNavigator from '../../src/navigation/AppNavigator';

// Mock the stack navigator
jest.mock('@react-navigation/stack', () => ({
  createStackNavigator: () => ({
    Navigator: ({ children }) => children,
    Screen: ({ name }) => name,
  }),
}));

// Mock the tab navigator
jest.mock('@react-navigation/bottom-tabs', () => ({
  createBottomTabNavigator: () => ({
    Navigator: ({ children }) => children,
    Screen: ({ name }) => name,
  }),
}));

// Mock @expo/vector-icons
jest.mock('@expo/vector-icons', () => ({
  Ionicons: 'Ionicons',
  MaterialCommunityIcons: 'MaterialCommunityIcons',
  FontAwesome: 'FontAwesome',
}));

// Mock screens
jest.mock('../../src/screens/HomeScreen', () => 'HomeScreen');
jest.mock('../../src/screens/LearningScreen', () => 'LearningScreen');
jest.mock('../../src/screens/NewsScreen', () => 'NewsScreen');
jest.mock('../../src/screens/QuestionsScreen', () => 'QuestionsScreen');
jest.mock('../../src/screens/LearningDetailScreen', () => 'LearningDetailScreen');
jest.mock('../../src/screens/NewsDetailScreen', () => 'NewsDetailScreen');
jest.mock('../../src/screens/QuestionDetailScreen', () => 'QuestionDetailScreen');
jest.mock('../../src/screens/AiChatScreen', () => 'AiChatScreen');

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