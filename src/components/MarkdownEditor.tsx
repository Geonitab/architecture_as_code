import { Editor } from '@toast-ui/react-editor';
import { useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Save, X } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import '@toast-ui/editor/dist/toastui-editor.css';

interface MarkdownEditorProps {
  content: string;
  title: string;
  onSave: (content: string) => void;
  onCancel: () => void;
}

const MarkdownEditor = ({ content, title, onSave, onCancel }: MarkdownEditorProps) => {
  const editorRef = useRef<Editor>(null);
  const { toast } = useToast();

  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.getInstance().setMarkdown(content);
    }
  }, [content]);

  const handleSave = () => {
    if (editorRef.current) {
      const markdownContent = editorRef.current.getInstance().getMarkdown();
      onSave(markdownContent);
      toast({
        title: "Sparat",
        description: "Kapitlet har sparats framgångsrikt.",
      });
    }
  };

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-6xl h-full max-h-[90vh] flex flex-col">
        <CardHeader className="border-b">
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl">Redigera: {title}</CardTitle>
            <div className="flex gap-2">
              <Button onClick={handleSave} size="sm" className="gap-2">
                <Save className="h-4 w-4" />
                Spara
              </Button>
              <Button onClick={onCancel} variant="outline" size="sm" className="gap-2">
                <X className="h-4 w-4" />
                Avbryt
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="flex-1 p-0 overflow-hidden">
          <div className="h-full">
            <Editor
              ref={editorRef}
              initialValue={content}
              previewStyle="vertical"
              height="100%"
              initialEditType="markdown"
              useCommandShortcut={true}
              hideModeSwitch={false}
              toolbarItems={[
                ['heading', 'bold', 'italic', 'strike'],
                ['hr', 'quote'],
                ['ul', 'ol', 'task', 'indent', 'outdent'],
                ['table', 'image', 'link'],
                ['code', 'codeblock'],
                ['scrollSync']
              ]}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MarkdownEditor;