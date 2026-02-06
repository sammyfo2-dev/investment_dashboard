import React, { useState, useCallback } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { useScreenshots } from '@/hooks/useScreenshots';
import { Upload, X } from 'lucide-react';

export const ScreenshotUpload: React.FC = () => {
  const { uploadScreenshot, isUploading } = useScreenshots();
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);

      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFile(e.dataTransfer.files[0]);
      }
    },
    []
  );

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  }, []);

  const handleFile = (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file');
      return;
    }

    uploadScreenshot(file);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Screenshot</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-primary bg-primary/5'
              : 'border-gray-300 hover:border-primary'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept="image/*"
            onChange={handleChange}
            disabled={isUploading}
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center"
          >
            <Upload className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-lg font-medium mb-2">
              {isUploading ? 'Uploading...' : 'Drop screenshot here'}
            </p>
            <p className="text-sm text-muted-foreground">
              or click to browse
            </p>
          </label>
        </div>

        <div className="mt-4 text-sm text-muted-foreground">
          <p>Upload investment advice screenshots from X/Twitter</p>
          <p>Free OCR will extract tickers and key text instantly</p>
        </div>
      </CardContent>
    </Card>
  );
};
