import { jest } from '@jest/globals';
// Mock react-native-gesture-handler
jest.mock('react-native-gesture-handler', () => import('./__mocks__/react-native-gesture-handler')); 