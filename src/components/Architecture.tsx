import React from 'react';
import { Database, MessageCircle, Cpu, Globe, Filter, Send } from 'lucide-react';

const Architecture = () => {
  const components = [
    {
      icon: MessageCircle,
      title: 'Data Loaders',
      description: 'Telegram channel monitoring and message extraction',
      color: 'bg-blue-500',
    },
    {
      icon: Globe,
      title: 'Translator',
      description: 'Multi-language translation with fallback mechanisms',
      color: 'bg-green-500',
    },
    {
      icon: Filter,
      title: 'Classifier',
      description: 'AI-powered content categorization and filtering',
      color: 'bg-purple-500',
    },
    {
      icon: Cpu,
      title: 'Message Manager',
      description: 'User preference matching and message routing',
      color: 'bg-orange-500',
    },
    {
      icon: Send,
      title: 'Telegram Bots',
      description: 'User interaction and message delivery',
      color: 'bg-red-500',
    },
    {
      icon: Database,
      title: 'Storage Layer',
      description: 'MongoDB, Redis, and Elasticsearch integration',
      color: 'bg-indigo-500',
    },
  ];

  return (
    <section id="architecture" className="section-padding bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Microservices Architecture
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            A scalable, event-driven architecture built with Docker containers, 
            Kafka messaging, and comprehensive monitoring through Elasticsearch and Kibana.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {components.map((component, index) => (
            <div
              key={component.title}
              className="card p-8 hover:scale-105 transform transition-all duration-300"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className={`${component.color} p-4 rounded-full w-16 h-16 flex items-center justify-center mb-6`}>
                <component.icon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                {component.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {component.description}
              </p>
            </div>
          ))}
        </div>

        {/* Architecture Flow */}
        <div className="mt-16 p-8 bg-white rounded-2xl shadow-lg">
          <h3 className="text-2xl font-bold text-center mb-8">Data Flow</h3>
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0 md:space-x-4">
            <div className="flex flex-col items-center text-center">
              <div className="bg-blue-100 p-3 rounded-full mb-2">
                <MessageCircle className="h-6 w-6 text-blue-600" />
              </div>
              <span className="text-sm font-medium">Data Collection</span>
            </div>
            <div className="hidden md:block text-gray-400">→</div>
            <div className="flex flex-col items-center text-center">
              <div className="bg-green-100 p-3 rounded-full mb-2">
                <Globe className="h-6 w-6 text-green-600" />
              </div>
              <span className="text-sm font-medium">Translation</span>
            </div>
            <div className="hidden md:block text-gray-400">→</div>
            <div className="flex flex-col items-center text-center">
              <div className="bg-purple-100 p-3 rounded-full mb-2">
                <Filter className="h-6 w-6 text-purple-600" />
              </div>
              <span className="text-sm font-medium">Classification</span>
            </div>
            <div className="hidden md:block text-gray-400">→</div>
            <div className="flex flex-col items-center text-center">
              <div className="bg-orange-100 p-3 rounded-full mb-2">
                <Cpu className="h-6 w-6 text-orange-600" />
              </div>
              <span className="text-sm font-medium">Processing</span>
            </div>
            <div className="hidden md:block text-gray-400">→</div>
            <div className="flex flex-col items-center text-center">
              <div className="bg-red-100 p-3 rounded-full mb-2">
                <Send className="h-6 w-6 text-red-600" />
              </div>
              <span className="text-sm font-medium">Delivery</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Architecture;