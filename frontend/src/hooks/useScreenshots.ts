import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { screenshotService } from '@/services/screenshotService';

export const useScreenshots = () => {
  const queryClient = useQueryClient();

  const screenshotsQuery = useQuery({
    queryKey: ['screenshots'],
    queryFn: screenshotService.getScreenshots,
  });

  const uploadMutation = useMutation({
    mutationFn: (file: File) => screenshotService.uploadScreenshot(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['screenshots'] });
    },
  });

  const analyzeMutation = useMutation({
    mutationFn: (screenshotId: number) => screenshotService.analyzeScreenshot(screenshotId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['screenshots'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (screenshotId: number) => screenshotService.deleteScreenshot(screenshotId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['screenshots'] });
    },
  });

  return {
    screenshots: screenshotsQuery.data || [],
    isLoading: screenshotsQuery.isLoading,
    error: screenshotsQuery.error,
    uploadScreenshot: uploadMutation.mutate,
    analyzeScreenshot: analyzeMutation.mutate,
    deleteScreenshot: deleteMutation.mutate,
    isUploading: uploadMutation.isPending,
    isAnalyzing: analyzeMutation.isPending,
  };
};
