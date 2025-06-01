import React from 'react';
import { View } from 'react-native';

// Mock gesture handlers
export const PanGestureHandler = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;
export const TapGestureHandler = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;
export const LongPressGestureHandler = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;
export const PinchGestureHandler = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;
export const RotationGestureHandler = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;
export const FlingGestureHandler = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;
export const ForceTouchGestureHandler = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;

// Mock states
export const State = {
  UNDETERMINED: 0,
  FAILED: 1,
  BEGAN: 2,
  CANCELLED: 3,
  ACTIVE: 4,
  END: 5,
};

// Mock directions
export const Directions = {
  RIGHT: 1,
  LEFT: 2,
  UP: 4,
  DOWN: 8,
};

// Mock methods
export const createNativeWrapper = (component: React.ComponentType<any>) => component;
export const gestureHandlerRootHOC = (component: React.ComponentType<any>) => component;

// Mock GestureHandlerRootView
export const GestureHandlerRootView = ({ children }: { children: React.ReactNode }) => <View>{children}</View>;

// Mock RNGestureHandlerModule
export const RNGestureHandlerModule = {
  attachGestureHandler: () => {},
  createGestureHandler: () => {},
  dropGestureHandler: () => {},
  updateGestureHandler: () => {},
  flushOperations: () => {},
};

// Mock default export
export default {
  PanGestureHandler,
  TapGestureHandler,
  LongPressGestureHandler,
  PinchGestureHandler,
  RotationGestureHandler,
  FlingGestureHandler,
  ForceTouchGestureHandler,
  State,
  Directions,
  createNativeWrapper,
  gestureHandlerRootHOC,
  GestureHandlerRootView,
  RNGestureHandlerModule,
}; 