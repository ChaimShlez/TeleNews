import React from 'react';
import { 
  Zap, 
  Shield, 
  Globe, 
  Users, 
  BarChart3, 
  Layers,
  Clock,
  Smartphone
} from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: Zap,
      title: 'Real-time Processing',
      description: 'Instant message processing with Apache Kafka streaming and Redis caching for optimal performance.',
    },
    {
      icon: Shield,
      title: 'Content Moderation',
      description: 'Advanced AI-powered content filtering and channel validation to ensure quality and safety.',
    },
    {
      icon: Globe,
      title: 'Multi-language Support',
      description: 'Automatic language detection and translation with multiple API fallbacks for reliability.',
    },
    {
      icon: Users,
      title: 'User Preferences',
      description: 'Personalized content delivery based on user-selected topics and interests.',
    },
    {
      icon: BarChart3,
      title: 'Analytics & Monitoring',
      description: 'Comprehensive logging and monitoring with Elasticsearch and Kibana dashboards.',
    },
    {
      icon: Layers,
      title: 'Microservices Architecture',
      description: 'Scalable, maintainable architecture with independent service deployment.',
    },
    {
      icon: Clock,
      title: 'Automated Workflows',
      description: 'CI/CD pipelines with GitHub Actions for automated testing and deployment.',
    },
    {
      icon: Smartphone,
      title: 'Telegram Integration',
      description: 'Native Telegram bot integration for seamless user interaction and content delivery.',
    },
  ];

  return (
    <section id="features" className="section-padding bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Platform Features
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Built with modern technologies and best practices to deliver 
            a robust, scalable, and user-friendly news distribution platform.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="card p-6 text-center hover:scale-105 transform transition-all duration-300"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="bg-primary-100 p-4 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <feature.icon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Statistics */}
        <div className="mt-16 grid md:grid-cols-4 gap-8 text-center">
          <div className="p-6">
            <div className="text-3xl font-bold text-primary-600 mb-2">7</div>
            <div className="text-gray-600">Microservices</div>
          </div>
          <div className="p-6">
            <div className="text-3xl font-bold text-primary-600 mb-2">10+</div>
            <div className="text-gray-600">Content Categories</div>
          </div>
          <div className="p-6">
            <div className="text-3xl font-bold text-primary-600 mb-2">24/7</div>
            <div className="text-gray-600">Monitoring</div>
          </div>
          <div className="p-6">
            <div className="text-3xl font-bold text-primary-600 mb-2">∞</div>
            <div className="text-gray-600">Scalability</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;