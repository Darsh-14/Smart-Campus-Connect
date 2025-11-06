import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import api from '../utils/api';
import { toast } from 'react-toastify';
import { Plus, FileText, Video } from 'lucide-react';

const AdminDashboard = () => {
  const [resources, setResources] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    resource_type: 'pdf',
    link: '',
  });

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const response = await api.get('/admin/resources');
      setResources(response.data);
    } catch (error) {
      toast.error('Failed to fetch resources');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/admin/resources', formData);
      toast.success('Resource created successfully!');
      setShowForm(false);
      setFormData({ title: '', resource_type: 'pdf', link: '' });
      fetchResources();
    } catch (error) {
      toast.error('Failed to create resource');
    }
  };

  const deleteResource = async (id) => {
    if (!confirm('Are you sure you want to delete this resource?')) return;
    try {
      await api.delete(`/admin/resources/${id}`);
      toast.success('Resource deleted successfully!');
      fetchResources();
    } catch (error) {
      toast.error('Failed to delete resource');
    }
  };

  return (
    <Layout title="Admin Dashboard">
      <div className="mb-6">
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Add Resource
        </button>
      </div>

      {showForm && (
        <div className="card mb-6">
          <h3 className="text-xl font-semibold mb-4">New Resource</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <input
                type="text"
                required
                className="input"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                className="input"
                value={formData.resource_type}
                onChange={(e) =>
                  setFormData({ ...formData, resource_type: e.target.value })
                }
              >
                <option value="pdf">PDF</option>
                <option value="video">Video</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Link
              </label>
              <input
                type="url"
                required
                className="input"
                value={formData.link}
                onChange={(e) => setFormData({ ...formData, link: e.target.value })}
                placeholder="https://..."
              />
            </div>

            <div className="flex gap-2">
              <button type="submit" className="btn btn-primary">
                Create
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="space-y-4">
        <h3 className="text-xl font-semibold">Resources</h3>
        {resources.length === 0 ? (
          <p className="text-gray-500">No resources available</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {resources.map((resource) => (
              <div key={resource.id} className="card relative">
                <div className="flex items-start gap-3">
                  {resource.resource_type === 'pdf' ? (
                    <FileText className="w-8 h-8 text-red-500" />
                  ) : (
                    <Video className="w-8 h-8 text-blue-500" />
                  )}
                  <div className="flex-1">
                    <h4 className="font-semibold">{resource.title}</h4>
                    <a
                      href={resource.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-primary-600 hover:underline"
                    >
                      View Resource
                    </a>
                  </div>
                </div>
                <button
                  onClick={() => deleteResource(resource.id)}
                  className="absolute top-4 right-4 text-red-600 hover:text-red-700 text-sm font-medium"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default AdminDashboard;
