import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TextInput, 
  TouchableOpacity, 
  FlatList, 
  KeyboardAvoidingView, 
  Platform,
  SafeAreaView,
  ActivityIndicator
} from 'react-native';
import api from '../utils/api';

// 聊天消息类型
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

const AiChatScreen = ({ route }: any) => {
  // 如果从其他屏幕传入了初始问题，则设置为初始输入
  const initialQuestion = route.params?.initialQuestion || '';
  
  const [input, setInput] = useState(initialQuestion);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '你好！我是你的财经智能助手。有什么财经问题需要我解答吗？',
      sender: 'ai',
      timestamp: new Date(),
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 发送消息并获取AI回复
  const sendMessage = async () => {
    if (input.trim() === '') return;
    
    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);
    
    try {
      // 准备历史消息数据
      const history = messages.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      }));
      
      // 调用API
      const response = await api.chat.send(input, history);
      
      // 添加AI回复
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.response,
        sender: 'ai',
        timestamp: new Date(),
      };
      
      setMessages(prevMessages => [...prevMessages, aiMessage]);
    } catch (err) {
      console.error('AI回复请求失败:', err);
      setError('无法获取AI回复，请重试');
      
      // 错误提示作为系统消息
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: '抱歉，我暂时无法回答，请稍后再试。',
        sender: 'ai',
        timestamp: new Date(),
      };
      
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // 渲染消息项
  const renderMessageItem = ({ item }: { item: Message }) => (
    <View style={[
      styles.messageBubble,
      item.sender === 'user' ? styles.userBubble : styles.aiBubble
    ]}>
      <Text style={styles.messageText}>{item.text}</Text>
      <Text style={styles.timestamp}>
        {item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>AI财经助手</Text>
      </View>
      
      <FlatList
        data={messages}
        renderItem={renderMessageItem}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.messageList}
        inverted={false}
      />
      
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={90}
      >
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            value={input}
            onChangeText={setInput}
            placeholder="输入你的财经问题..."
            multiline
          />
          <TouchableOpacity 
            style={[styles.sendButton, (!input.trim() || isLoading) && styles.disabledButton]}
            onPress={sendMessage}
            disabled={!input.trim() || isLoading}
          >
            {isLoading ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <Text style={styles.sendButtonText}>发送</Text>
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
      
      <View style={styles.disclaimer}>
        <Text style={styles.disclaimerText}>
          AI助手仅提供一般性信息，不构成投资建议。实际投资需谨慎。
        </Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 15,
    backgroundColor: '#3498db',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  messageList: {
    paddingHorizontal: 15,
    paddingBottom: 10,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 18,
    marginVertical: 8,
  },
  userBubble: {
    backgroundColor: '#3498db',
    alignSelf: 'flex-end',
    borderBottomRightRadius: 4,
  },
  aiBubble: {
    backgroundColor: 'white',
    alignSelf: 'flex-start',
    borderBottomLeftRadius: 4,
  },
  messageText: {
    fontSize: 16,
    color: '#333',
  },
  timestamp: {
    fontSize: 10,
    color: '#888',
    alignSelf: 'flex-end',
    marginTop: 4,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  input: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    maxHeight: 120,
  },
  sendButton: {
    backgroundColor: '#3498db',
    width: 70,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 10,
    paddingVertical: 10,
  },
  sendButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  disabledButton: {
    backgroundColor: '#b3d1e6',
  },
  disclaimer: {
    padding: 10,
    backgroundColor: '#f8f8f8',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  disclaimerText: {
    fontSize: 10,
    color: '#888',
    textAlign: 'center',
  },
});

export default AiChatScreen; 