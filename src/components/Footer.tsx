import React from 'react';
import { MessageSquare, Github, ExternalLink, Mail } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white section-padding">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="col-span-1">
            <div className="flex items-center space-x-2 mb-4">
              <MessageSquare className="h-8 w-8 text-primary-400" />
              <span className="text-2xl font-bold">TeleNews</span>
            </div>
            <p className="text-gray-400 leading-relaxed">
              Intelligent news distribution platform built with microservices architecture 
              for scalable, real-time content delivery.
            </p>
          </div>

          {/* Architecture */}
          <div>
            <h3 className="font-semibold text-lg mb-4">Architecture</h3>
            <ul className="space-y-2 text-gray-400">
              <li>Microservices Design</li>
              <li>Event-Driven Processing</li>
              <li>Container Orchestration</li>
              <li>Real-time Messaging</li>
            </ul>
          </div>

          {/* Technologies */}
          <div>
            <h3 className="font-semibold text-lg mb-4">Technologies</h3>
            <ul className="space-y-2 text-gray-400">
              <li>Python & FastAPI</li>
              <li>Apache Kafka</li>
              <li>Docker & Kubernetes</li>
              <li>MongoDB & Redis</li>
            </ul>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-lg mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="#architecture" className="text-gray-400 hover:text-primary-400 transition-colors flex items-center">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Documentation
                </a>
              </li>
              <li>
                <a href="#services" className="text-gray-400 hover:text-primary-400 transition-colors flex items-center">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  API Reference
                </a>
              </li>
              <li>
                <a href="#deployment" className="text-gray-400 hover:text-primary-400 transition-colors flex items-center">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Deployment Guide
                </a>
              </li>
              <li>
                <a href="mailto:contact@telenews.dev" className="text-gray-400 hover:text-primary-400 transition-colors flex items-center">
                  <Mail className="h-4 w-4 mr-2" />
                  Contact
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © {currentYear} TeleNews. Built with modern microservices architecture.
          </p>
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <a
              href="https://github.com"
              className="text-gray-400 hover:text-primary-400 transition-colors"
              aria-label="GitHub Repository"
            >
              <Github className="h-5 w-5" />
            </a>
            <div className="flex items-center space-x-2 text-sm text-gray-400">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span>System Operational</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;