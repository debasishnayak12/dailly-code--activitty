import React from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import UploadForm from './components/UploadForm';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <UploadForm />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 50,
    paddingHorizontal: 10,
    backgroundColor: '#f0f0f0',
  },
});
