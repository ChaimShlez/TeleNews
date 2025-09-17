import React from 'react';
import { 
  Container, 
  GitBranch, 
  Play, 
  Settings, 
  CheckCircle,
  ExternalLink
} from 'lucide-react';

const Deployment = () => {
  const deploymentSteps = [
    {
      icon: GitBranch,
      title: 'Source Control',
      description: 'Code managed in GitHub with automated CI/CD workflows',
      details: ['GitHub Actions', 'Automated testing', 'Multi-branch support'],
    },
    {
      icon: Container,
      title: 'Containerization',
      description: 'Each service packaged in optimized Docker containers',
      details: ['Multi-stage builds', 'Layer caching', 'Security scanning'],
    },
    {
      icon: Settings,
      title: 'Orchestration',
      description: 'Kubernetes and Docker Compose for service management',
      details: ['Service discovery', 'Load balancing', 'Health checks'],
    },
    {
      icon: CheckCircle,
      title: 'Monitoring',
      description: 'Comprehensive logging and monitoring setup',
      details: ['Elasticsearch logs', 'Kibana dashboards', 'Real-time alerts'],
    },
  ];

  const commands = [
    {
      title: 'Quick Start with Docker Compose',
      command: 'cd infra/Docker && docker compose up',
      description: 'Launch the entire platform locally',
    },
    {
      title: 'Build and Push Images',
      command: './scriptes/bilud-posh.bat',
      description: 'Build and push all service images to Docker Hub',
    },
    {
      title: 'Kubernetes Deployment',
      command: 'kubectl apply -f services/',
      description: 'Deploy services to Kubernetes cluster',
    },
  ];

  return (
    <section id="deployment" className="section-padding bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Deployment & Operations
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Streamlined deployment process with Docker containers, 
            Kubernetes orchestration, and comprehensive monitoring.
          </p>
        </div>

        {/* Deployment Process */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {deploymentSteps.map((step, index) => (
            <div
              key={step.title}
              className="card p-6 text-center animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="bg-primary-100 p-4 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <step.icon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                {step.title}
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                {step.description}
              </p>
              <ul className="space-y-1">
                {step.details.map((detail, idx) => (
                  <li key={idx} className="text-xs text-gray-500 flex items-center justify-center">
                    <div className="w-1 h-1 bg-primary-400 rounded-full mr-2"></div>
                    {detail}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Command Examples */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <h3 className="text-2xl font-bold text-center mb-8">Deployment Commands</h3>
          <div className="space-y-6">
            {commands.map((cmd, index) => (
              <div
                key={cmd.title}
                className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <h4 className="font-semibold text-gray-900">{cmd.title}</h4>
                  <Play className="h-5 w-5 text-primary-600" />
                </div>
                <p className="text-gray-600 text-sm mb-3">{cmd.description}</p>
                <div className="bg-gray-900 text-green-400 p-3 rounded-lg font-mono text-sm">
                  {cmd.command}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Service Ports */}
        <div className="mt-16 grid md:grid-cols-2 gap-8">
          <div className="card p-8">
            <h3 className="text-xl font-semibold mb-6 flex items-center">
              <Settings className="h-6 w-6 mr-2 text-primary-600" />
              Service Ports
            </h3>
            <div className="space-y-3">
              {[
                { service: 'Kafka', port: '9092' },
                { service: 'Kafdrop', port: '9000' },
                { service: 'Elasticsearch', port: '9200' },
                { service: 'Kibana', port: '5601' },
                { service: 'MongoDB', port: '27017' },
                { service: 'Redis', port: '6379' },
              ].map((item) => (
                <div key={item.service} className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="font-medium text-gray-700">{item.service}</span>
                  <span className="text-primary-600 font-mono">{item.port}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-8">
            <h3 className="text-xl font-semibold mb-6 flex items-center">
              <ExternalLink className="h-6 w-6 mr-2 text-primary-600" />
              External Dependencies
            </h3>
            <div className="space-y-3">
              {[
                { name: 'Telegram API', purpose: 'Bot communication' },
                { name: 'Translation APIs', purpose: 'Multi-language support' },
                { name: 'Docker Hub', purpose: 'Image registry' },
                { name: 'GitHub Actions', purpose: 'CI/CD automation' },
              ].map((item) => (
                <div key={item.name} className="py-2 border-b border-gray-100">
                  <div className="font-medium text-gray-700">{item.name}</div>
                  <div className="text-sm text-gray-500">{item.purpose}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Deployment;