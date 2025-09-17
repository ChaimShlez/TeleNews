import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Architecture from './components/Architecture';
import Services from './components/Services';
import Features from './components/Features';
import TechStack from './components/TechStack';
import Deployment from './components/Deployment';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <Header />
      <Hero />
      <Architecture />
      <Services />
      <Features />
      <TechStack />
      <Deployment />
      <Footer />
    </div>
  );
}

export default App;