import React from 'react';
import { ArrowRight, Zap, Globe, Shield } from 'lucide-react';

const Hero = () => {
  return (
    <section className="pt-24 pb-16 section-padding">
      <div className="max-w-7xl mx-auto">
        <div className="text-center animate-fade-in">
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Intelligent News
            <span className="text-primary-600 block">Distribution Platform</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            A sophisticated microservices architecture for collecting, translating, classifying, 
            and distributing news content through Telegram channels with real-time processing.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <a href="#architecture" className="btn-primary inline-flex items-center">
              Explore Architecture
              <ArrowRight className="ml-2 h-5 w-5" />
            </a>
            <a href="#services" className="btn-secondary">
              View Services
            </a>
          </div>

          {/* Key Features */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="flex flex-col items-center p-6 animate-slide-up">
              <div className="bg-primary-100 p-4 rounded-full mb-4">
                <Zap className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Real-time Processing</h3>
              <p className="text-gray-600 text-center">
                Instant message processing with Kafka streaming and Redis caching
              </p>
            </div>
            
            <div className="flex flex-col items-center p-6 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="bg-primary-100 p-4 rounded-full mb-4">
                <Globe className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Multi-language Support</h3>
              <p className="text-gray-600 text-center">
                Automatic translation and language detection for global news coverage
              </p>
            </div>
            
            <div className="flex flex-col items-center p-6 animate-slide-up" style={{ animationDelay: '0.4s' }}>
              <div className="bg-primary-100 p-4 rounded-full mb-4">
                <Shield className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Content Filtering</h3>
              <p className="text-gray-600 text-center">
                AI-powered classification and content moderation for quality assurance
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;