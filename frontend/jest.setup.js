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

// 完整模拟 React Native
jest.mock('react-native', () => {
  const rn = jest.requireActual('react-native');
  
  // 确保 ExpoFontLoader 存在
  if (!rn.NativeModules) {
    rn.NativeModules = {};
  }
  rn.NativeModules.ExpoFontLoader = {
    loadAsync: jest.fn(() => Promise.resolve()),
  };
  
  // 模拟 TurboModuleRegistry
  rn.TurboModuleRegistry = {
    get: jest.fn(() => null),
    getEnforcing: jest.fn((name) => {
      // 返回所有可能需要的模块
      if (name === 'DevMenu') {
        return {
          show: jest.fn(),
          reload: jest.fn(),
          setProfilingEnabled: jest.fn(),
          setHotLoadingEnabled: jest.fn()
        };
      }
      // 添加其他可能需要的模块
      return {}; // 返回空对象而不是 null，避免空引用错误
    })
  };
  
  // 确保 VirtualizedList 相关组件正确模拟
  const mockComponent = (name) => {
    const Component = ({children}) => children || null;
    Component.displayName = name;
    return Component;
  };
  
  return {
    ...rn,
    NativeModules: {
      ...rn.NativeModules,
      ExpoFontLoader: {
        loadAsync: jest.fn(() => Promise.resolve()),
      },
    },
    // 添加 DevMenu 模拟
    DevMenu: {
      show: jest.fn(),
    },
    // 保留 TurboModuleRegistry 模拟
    TurboModuleRegistry: rn.TurboModuleRegistry,
    UIManager: {
      ...rn.UIManager,
      RCTView: () => ({}),
      getViewManagerConfig: jest.fn(() => null),
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
    FlatList: mockComponent('FlatList'),
    ActivityIndicator: mockComponent('ActivityIndicator'),
    Image: mockComponent('Image'),
    ScrollView: mockComponent('ScrollView'),
    SafeAreaView: mockComponent('SafeAreaView'),
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