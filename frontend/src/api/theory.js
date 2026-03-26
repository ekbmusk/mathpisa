import client from './client'

export const theoryAPI = {
  getTopics: () => client.get('/theory/topics'),
  getTopicDetail: (topicId) => client.get(`/theory/topics/${topicId}`),
  getSubtopics: (topicId) => client.get(`/theory/topics/${topicId}/subtopics`),
  getQuiz: (topicId, count = 5) => client.get(`/theory/topics/${topicId}/quiz?count=${count}`),
  submitQuiz: (data) => client.post('/theory/quiz/submit', data),
}
