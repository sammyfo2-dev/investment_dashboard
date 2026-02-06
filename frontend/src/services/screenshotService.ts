import api from './api';
import { Screenshot, ScreenshotUploadResponse, AIAnalysisResponse } from '@/types/screenshot';

export const screenshotService = {
  uploadScreenshot: async (file: File): Promise<ScreenshotUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/screenshots/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  analyzeScreenshot: async (screenshotId: number): Promise<AIAnalysisResponse> => {
    const response = await api.post(`/api/screenshots/${screenshotId}/analyze`);
    return response.data;
  },

  getScreenshots: async (): Promise<Screenshot[]> => {
    const response = await api.get('/api/screenshots');
    return response.data;
  },

  getScreenshot: async (screenshotId: number): Promise<Screenshot> => {
    const response = await api.get(`/api/screenshots/${screenshotId}`);
    return response.data;
  },

  deleteScreenshot: async (screenshotId: number): Promise<void> => {
    await api.delete(`/api/screenshots/${screenshotId}`);
  },
};
