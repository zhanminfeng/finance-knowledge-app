import '@testing-library/jest-native/extend-expect';
import { describe, it, expect } from '@jest/globals';
import React from 'react';
import { Text, View } from 'react-native';
import { render } from '@testing-library/react-native';

describe('Minimal Test', () => {
  it('renders correctly', () => {
    const { getByText } = render(
      <View>
        <Text>Hello, World!</Text>
      </View>
    );
    expect(getByText('Hello, World!')).toBeTruthy();
  });
});