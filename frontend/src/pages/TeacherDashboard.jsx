import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import api from '../utils/api';
import { toast } from 'react-toastify';
import { Plus } from 'lucide-react';

const TeacherDashboard = () => {
  const [assignments, setAssignments] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    due_date: '',
    meet_link: '',
  });

  useEffect(() => {
    fetchAssignments();
  }, []);

  const fetchAssignments = async () => {
    try {
      const response = await api.get('/teacher/assignments');
      setAssignments(response.data);
    } catch (error) {
      toast.error('Failed to fetch assignments');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/teacher/assignments', formData);
      toast.success('Assignment created successfully!');
      setShowForm(false);
      setFormData({ title: '', description: '', due_date: '', meet_link: '' });
      fetchAssignments();
    } catch (error) {
      toast.error('Failed to create assignment');
    }
  };

  const deleteAssignment = async (id) => {
    if (!confirm('Are you sure you want to delete this assignment?')) return;
    try {
      await api.delete(`/teacher/assignments/${id}`);
      toast.success('Assignment deleted successfully!');
      fetchAssignments();
    } catch (error) {
      toast.error('Failed to delete assignment');
    }
  };

  return (
    <Layout title="Teacher Dashboard">
      <div className="mb-6">
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Create Assignment
        </button>
      </div>

      {showForm && (
        <div className="card mb-6">
          <h3 className="text-xl font-semibold mb-4">New Assignment</h3>
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
                Description
              </label>
              <textarea
                required
                rows="4"
                className="input"
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Due Date
              </label>
              <input
                type="date"
                required
                className="input"
                value={formData.due_date}
                onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Meeting Link (Optional)
              </label>
              <input
                type="url"
                className="input"
                value={formData.meet_link}
                onChange={(e) => setFormData({ ...formData, meet_link: e.target.value })}
                placeholder="https://meet.google.com/..."
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
        <h3 className="text-xl font-semibold">My Assignments</h3>
        {assignments.length === 0 ? (
          <p className="text-gray-500">No assignments created yet</p>
        ) : (
          assignments.map((assignment) => (
            <div key={assignment.id} className="card">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-semibold text-lg">{assignment.title}</h4>
                  <p className="text-gray-600 mt-2">{assignment.description}</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Due: {new Date(assignment.due_date).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={() => deleteAssignment(assignment.id)}
                  className="text-red-600 hover:text-red-700 font-medium"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </Layout>
  );
};

export default TeacherDashboard;
