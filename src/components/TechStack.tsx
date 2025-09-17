import React from 'react';
import { Server, Database, MessageSquare, Cloud, Monitor, Code } from 'lucide-react';

const TechStack = () => {
  const categories = [
    {
      icon: Code,
      title: 'Languages & Frameworks',
      technologies: ['Python 3.10', 'FastAPI', 'Telethon', 'Scikit-learn', 'Sentence Transformers'],
      color: 'bg-blue-500',
    },
    {
      icon: MessageSquare,
      title: 'Messaging & Communication',
      technologies: ['Apache Kafka', 'Telegram Bot API', 'Redis Pub/Sub', 'WebSocket'],
      color: 'bg-green-500',
    },
    {
      icon: Database,
      title: 'Data Storage',
      technologies: ['MongoDB', 'Redis', 'Elasticsearch', 'Persistent Volumes'],
      color: 'bg-purple-500',
    },
    {
      icon: Cloud,
      title: 'Infrastructure',
      technologies: ['Docker', 'Kubernetes', 'GitHub Actions', 'Docker Hub'],
      color: 'bg-orange-500',
    },
    {
      icon: Monitor,
      title: 'Monitoring & Analytics',
      technologies: ['Kibana', 'Elasticsearch Logging', 'Kafdrop', 'Health Checks'],
      color: 'bg-red-500',
    },
    {
      icon: Server,
      title: 'DevOps & Deployment',
      technologies: ['Docker Compose', 'Kubernetes YAML', 'CI/CD Pipelines', 'Multi-stage Builds'],
      color: 'bg-indigo-500',
    },
  ];

  return (
    <section id="tech-stack" className="section-padding">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Technology Stack
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Built with cutting-edge technologies and industry best practices 
            for maximum performance, scalability, and reliability.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {categories.map((category, index) => (
            <div
              key={category.title}
              className="card p-8 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className={`${category.color} p-4 rounded-full w-16 h-16 flex items-center justify-center mb-6`}>
                <category.icon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {category.title}
              </h3>
              <div className="space-y-2">
                {category.technologies.map((tech, idx) => (
                  <div
                    key={idx}
                    className="bg-gray-50 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 inline-block mr-2 mb-2"
                  >
                    {tech}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Architecture Diagram */}
        <div className="mt-16 p-8 bg-gradient-to-r from-primary-50 to-secondary-50 rounded-2xl">
          <h3 className="text-2xl font-bold text-center mb-8">System Architecture</h3>
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div className="space-y-4">
              <div className="bg-white p-6 rounded-xl shadow-md">
                <h4 className="font-semibold text-gray-900 mb-2">Data Layer</h4>
                <p className="text-sm text-gray-600">MongoDB, Redis, Elasticsearch</p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="bg-white p-6 rounded-xl shadow-md">
                <h4 className="font-semibold text-gray-900 mb-2">Processing Layer</h4>
                <p className="text-sm text-gray-600">Kafka, Python Services, AI Models</p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="bg-white p-6 rounded-xl shadow-md">
                <h4 className="font-semibold text-gray-900 mb-2">Presentation Layer</h4>
                <p className="text-sm text-gray-600">Telegram Bots, FastAPI, Web Interface</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechStack;