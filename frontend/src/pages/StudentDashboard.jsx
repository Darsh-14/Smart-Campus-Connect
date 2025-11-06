import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import api from '../utils/api';
import { toast } from 'react-toastify';
import { BookOpen, Calendar, CheckCircle, FileText, Video } from 'lucide-react';
import { format } from 'date-fns';

const StudentDashboard = () => {
  const [assignments, setAssignments] = useState([]);
  const [resources, setResources] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [marks, setMarks] = useState([]);
  const [activeTab, setActiveTab] = useState('assignments');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [assignmentsRes, resourcesRes, attendanceRes, marksRes] = await Promise.all([
        api.get('/student/assignments'),
        api.get('/student/resources'),
        api.get('/student/attendance'),
        api.get('/student/marks'),
      ]);

      setAssignments(assignmentsRes.data);
      setResources(resourcesRes.data);
      setAttendance(attendanceRes.data);
      setMarks(marksRes.data);
    } catch (error) {
      toast.error('Failed to fetch data');
    }
  };

  const submitAssignment = async (assignmentId) => {
    try {
      await api.post(`/student/assignments/${assignmentId}/submit`);
      toast.success('Assignment submitted successfully!');
      fetchData();
    } catch (error) {
      toast.error('Failed to submit assignment');
    }
  };

  return (
    <Layout title="Student Dashboard">
      {/* Tabs */}
      <div className="flex space-x-4 mb-6 border-b">
        {['assignments', 'resources', 'attendance', 'marks'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 font-medium capitalize ${
              activeTab === tab
                ? 'border-b-2 border-primary-600 text-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Assignments Tab */}
      {activeTab === 'assignments' && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold mb-4">My Assignments</h3>
          {assignments.length === 0 ? (
            <p className="text-gray-500">No assignments available</p>
          ) : (
            assignments.map((assignment) => (
              <div key={assignment.id} className="card">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-semibold text-lg">{assignment.title}</h4>
                    <p className="text-gray-600 mt-2">{assignment.description}</p>
                    <div className="flex items-center gap-4 mt-3 text-sm text-gray-500">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        Due: {format(new Date(assignment.due_date), 'PPP')}
                      </span>
                      {assignment.meet_link && (
                        <a
                          href={assignment.meet_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-1 text-primary-600 hover:underline"
                        >
                          <Video className="w-4 h-4" />
                          Join Meeting
                        </a>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => submitAssignment(assignment.id)}
                    className="btn btn-primary ml-4"
                  >
                    Submit
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Resources Tab */}
      {activeTab === 'resources' && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold mb-4">Study Resources</h3>
          {resources.length === 0 ? (
            <p className="text-gray-500">No resources available</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {resources.map((resource) => (
                <a
                  key={resource.id}
                  href={resource.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="card hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-start gap-3">
                    {resource.resource_type === 'pdf' ? (
                      <FileText className="w-8 h-8 text-red-500" />
                    ) : (
                      <Video className="w-8 h-8 text-blue-500" />
                    )}
                    <div>
                      <h4 className="font-semibold">{resource.title}</h4>
                      <span className="text-sm text-gray-500 capitalize">
                        {resource.resource_type}
                      </span>
                    </div>
                  </div>
                </a>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Attendance Tab */}
      {activeTab === 'attendance' && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold mb-4">My Attendance</h3>
          {attendance.length === 0 ? (
            <p className="text-gray-500">No attendance records</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {attendance.map((record) => (
                <div key={record.id} className="card">
                  <h4 className="font-semibold text-lg">{record.subject}</h4>
                  <div className="mt-3 flex items-center justify-between">
                    <span className="text-gray-600">
                      Present: {record.present_days} / {record.total_days}
                    </span>
                    <span
                      className={`font-semibold ${
                        (record.present_days / record.total_days) * 100 >= 75
                          ? 'text-green-600'
                          : 'text-red-600'
                      }`}
                    >
                      {((record.present_days / record.total_days) * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Marks Tab */}
      {activeTab === 'marks' && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold mb-4">My Marks</h3>
          {marks.length === 0 ? (
            <p className="text-gray-500">No marks available</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {marks.map((mark) => (
                <div key={mark.id} className="card">
                  <h4 className="font-semibold text-lg">{mark.subject}</h4>
                  <div className="mt-3 flex items-center justify-between">
                    <span className="text-gray-600">
                      Marks: {mark.marks_obtained} / {mark.total_marks}
                    </span>
                    <span className="font-semibold text-primary-600">
                      {((mark.marks_obtained / mark.total_marks) * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </Layout>
  );
};

export default StudentDashboard;
