import { jest } from '@jest/globals';
import React from 'react'; // 确保这一行存在

// Mock react-native-gesture-handler
jest.mock('react-native-gesture-handler', () => import('./__mocks__/react-native-gesture-handler'));

// Import Jest Native matchers
import '@testing-library/jest-native/extend-expect';
import { act } from 'react-test-renderer';

// Mock @expo/vector-icons
jest.mock('@expo/vector-icons', () => {
  const { View } = require('react-native');
  return {
    Ionicons: View,
    MaterialCommunityIcons: View,
    FontAwesome: View,
    createIconSet: () => View,
  };
});

// Mock react-native-vector-icons
jest.mock('react-native-vector-icons/FontAwesome5', () => 'FontAwesome5Icon');
jest.mock('react-native-vector-icons/MaterialIcons', () => 'MaterialIconsIcon');
jest.mock('react-native-vector-icons/Ionicons', () => 'IoniconsIcon');

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () => ({
  setItem: jest.fn(() => Promise.resolve()),
  getItem: jest.fn(() => Promise.resolve()),
  removeItem: jest.fn(() => Promise.resolve()),
  clear: jest.fn(() => Promise.resolve()),
}));

// Mock navigation
jest.mock('@react-navigation/native', () => {
  const actualNav = jest.requireActual('@react-navigation/native');
  return {
    ...actualNav,
    useNavigation: () => ({
      navigate: jest.fn(),
      goBack: jest.fn(),
    }),
    useRoute: () => ({
      params: {
        itemId: '123',
      },
    }),
    NavigationContainer: ({ children }) => children,
  };
});

// Mock stack navigator
jest.mock('@react-navigation/stack', () => {
  const actualNav = jest.requireActual('@react-navigation/stack');
  return {
    ...actualNav,
    createStackNavigator: () => ({
      Navigator: ({ children }) => children,
      Screen: ({ name }) => name,
    }),
    TransitionPresets: {
      SlideFromRightIOS: {},
      ModalSlideFromBottomIOS: {},
    },
    TransitionSpecs: {
      TransitionIOSSpec: {},
    },
    HeaderStyleInterpolators: {
      forUIKit: {},
    },
    CardStyleInterpolators: {
      forHorizontalIOS: {},
      forVerticalIOS: {},
      forModalPresentationIOS: {},
    },
  };
});

// Mock bottom tabs navigator
jest.mock('@react-navigation/bottom-tabs', () => ({
  createBottomTabNavigator: () => ({
    Navigator: ({ children }) => children,
    Screen: ({ name }) => name,
  }),
}));

// Mock @react-native/virtualized-lists
// 修改第一处（大约在第90-95行）
jest.mock('@react-native/virtualized-lists', () => {
  const mockComponent = (name) => {
    const Component = ({children, ...props}) => {
      const React = require('react'); // 在函数内部引入 React
      return React.createElement('view', props, children);
    };
    Component.displayName = name;
    return Component;
  };
  
  return {
    VirtualizedList: mockComponent('VirtualizedList'),
    VirtualizedSectionList: mockComponent('VirtualizedSectionList'),
    keyExtractor: (item) => item.key || item.id || String(item),
    VirtualizedListContextResetter: ({children}) => children,
    ViewabilityHelper: function() {
      this.onUpdate = jest.fn();
      this.computeViewableItems = jest.fn().mockReturnValue([]);
      return this;
    },
    FillRateHelper: function() {
      this.activate = jest.fn();
      this.deactivateAndFlush = jest.fn();
      return this;
    },
  };
});

// 修改第二处（大约在第125-135行）
// 这里是 mockComponent 函数的定义
const mockComponent = (name) => {
  const Component = ({children, ...props}) => {
    const React = require('react'); // 在函数内部引入 React
    return React.createElement(name.toLowerCase(), props, children);
  };
  Component.displayName = name;
  return Component;
};
// 完整模拟 React Native
jest.mock('react-native', () => {
  const rn = jest.requireActual('react-native');
  const React = require('react');
  
  // 确保 NativeModules 存在
  if (!rn.NativeModules) {
    rn.NativeModules = {};
  }
  
  // 创建一个更健壮的 mockComponent 函数
  const mockComponent = (name) => {
    const Component = ({children, ...props}) => {
      return React.createElement(name.toLowerCase(), props, children);
    };
    Component.displayName = name;
    return Component;
  };
  
  // 创建 DevMenu 模块
  const DevMenuModule = {
    show: jest.fn(),
    reload: jest.fn(),
    debugRemotely: jest.fn(),
    setProfilingEnabled: jest.fn(),
    setHotLoadingEnabled: jest.fn(),
  };
  
  // 模拟 TurboModuleRegistry
  const mockTurboModuleRegistry = {
    get: jest.fn((name) => {
      if (name === 'DevMenu') {
        return DevMenuModule;
      }
      return null;
    }),
    
    // 在 TurboModuleRegistry.getEnforcing 中添加
    getEnforcing: jest.fn((name) => {
      console.log(`TurboModuleRegistry.getEnforcing called with: ${name}`);
      if (name === 'DevMenu') {
        console.log('Returning DevMenuModule');
        return DevMenuModule;
      }
      console.log(`Returning empty object for: ${name}`);
      return {};
    }),
  };
  
  return {
    ...rn,
    NativeModules: {
      ...rn.NativeModules,
      ExpoFontLoader: {
        loadAsync: jest.fn(() => Promise.resolve()),
      },
      // 添加 DevMenu 到 NativeModules
      DevMenu: DevMenuModule,
    },
    // 添加 DevMenu 模拟
    DevMenu: DevMenuModule,
    // 替换 TurboModuleRegistry 模拟
    TurboModuleRegistry: mockTurboModuleRegistry,
    UIManager: {
      ...rn.UIManager,
      RCTView: () => ({}),
      getViewManagerConfig: jest.fn((name) => {
        if (name === 'RCTView') {
          return {};
        }
        return null;
      }),
      measure: jest.fn(),
      measureInWindow: jest.fn(),
    },
    StyleSheet: {
      ...rn.StyleSheet,
      create: (styles) => styles,
      hairlineWidth: 1,
      absoluteFill: {},
      flatten: jest.fn(styles => styles),
    },
    Animated: {
      ...rn.Animated,
      createAnimatedComponent: (component) => component,
      timing: () => ({
        start: (callback) => callback && callback(),
      }),
      Value: function() {
        this.setValue = jest.fn();
        this.interpolate = jest.fn(() => ({ interpolate: jest.fn() }));
        return this;
      },
    },
    Platform: {
      ...rn.Platform,
      OS: 'ios',
      select: jest.fn((obj) => obj.ios),
    },
    // 使用 mockComponent 确保组件正确渲染
    View: mockComponent('View'),
    Text: mockComponent('Text'),
    TouchableOpacity: mockComponent('TouchableOpacity'),
    ActivityIndicator: mockComponent('ActivityIndicator'),
    Image: mockComponent('Image'),
    ScrollView: mockComponent('ScrollView'),
    SafeAreaView: mockComponent('SafeAreaView'),
    // 显式添加 VirtualizedList 和 FlatList
    VirtualizedList: mockComponent('VirtualizedList'),
    FlatList: mockComponent('FlatList'),
  };
}, {virtual: true});

// Global fetch mock
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
  })
);

// 添加全局辅助函数，用于包装异步更新
global.waitForComponentToPaint = async (wrapper) => {
  await act(async () => {
    await new Promise(resolve => setTimeout(resolve, 0));
    wrapper.update();
  });
};

// 在文件顶部添加
console.log('Loading root jest.setup.js');


// 修改 @expo/vector-icons 的模拟方式
try {
  jest.mock('@expo/vector-icons', () => {
    const { View } = require('react-native');
    return {
      Ionicons: View,
      MaterialCommunityIcons: View,
      FontAwesome: View,
      createIconSet: () => View,
    };
  });
} catch (error) {
  console.warn('无法模拟 @expo/vector-icons，可能模块不存在');
}