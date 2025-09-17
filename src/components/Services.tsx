import React from 'react';
import { Code, Settings, CheckCircle, AlertCircle } from 'lucide-react';

const Services = () => {
  const services = [
    {
      name: 'DataLoaders',
      description: 'Monitors Telegram channels and extracts messages with media support',
      features: ['Real-time message monitoring', 'Media file handling', 'Channel management', 'Redis caching'],
      status: 'active',
      port: '8000',
    },
    {
      name: 'Translator',
      description: 'Multi-language translation with fallback mechanisms',
      features: ['Language detection', 'Multiple translation APIs', 'Fallback strategies', 'Hebrew optimization'],
      status: 'active',
      port: '8001',
    },
    {
      name: 'Classifier',
      description: 'AI-powered content categorization using sentence transformers',
      features: ['Semantic analysis', 'Topic classification', 'Content filtering', 'Multilingual support'],
      status: 'active',
      port: '8002',
    },
    {
      name: 'ManagerMessage',
      description: 'Routes messages based on user preferences and topics',
      features: ['User preference matching', 'Message routing', 'MongoDB integration', 'Kafka consumption'],
      status: 'active',
      port: '8003',
    },
    {
      name: 'TelegramListener',
      description: 'Handles user interactions and preference management',
      features: ['User registration', 'Topic selection', 'Channel suggestions', 'Conversation handling'],
      status: 'active',
      port: '8004',
    },
    {
      name: 'TelegramSend',
      description: 'Delivers messages to users via Telegram API',
      features: ['Message delivery', 'Media support', 'Batch processing', 'Error handling'],
      status: 'active',
      port: '8005',
    },
    {
      name: 'CheckService',
      description: 'Content moderation and channel validation',
      features: ['Content filtering', 'Channel approval', 'Blacklist management', 'Quality assurance'],
      status: 'development',
      port: '8006',
    },
  ];

  return (
    <section id="services" className="section-padding">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Microservices Overview
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Each service is containerized and independently deployable, 
            ensuring scalability and maintainability across the platform.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {services.map((service, index) => (
            <div
              key={service.name}
              className="card p-8 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="bg-primary-100 p-3 rounded-lg">
                    <Code className="h-6 w-6 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">
                      {service.name}
                    </h3>
                    <p className="text-sm text-gray-500">Port: {service.port}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {service.status === 'active' ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <AlertCircle className="h-5 w-5 text-yellow-500" />
                  )}
                  <span className={`text-sm font-medium ${
                    service.status === 'active' ? 'text-green-600' : 'text-yellow-600'
                  }`}>
                    {service.status === 'active' ? 'Active' : 'Development'}
                  </span>
                </div>
              </div>

              <p className="text-gray-600 mb-6 leading-relaxed">
                {service.description}
              </p>

              <div className="space-y-2">
                <h4 className="font-medium text-gray-900 flex items-center">
                  <Settings className="h-4 w-4 mr-2" />
                  Key Features
                </h4>
                <ul className="space-y-1">
                  {service.features.map((feature, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-center">
                      <div className="w-1.5 h-1.5 bg-primary-400 rounded-full mr-3"></div>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;