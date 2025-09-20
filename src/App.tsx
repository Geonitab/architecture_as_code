import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import BookOverview from "./pages/BookOverview";
import ChaptersOverview from "./pages/ChaptersOverview";
import ChapterDetail from "./pages/ChapterDetail";
import Contact from "./pages/Contact";
import Resources from "./pages/Resources";
import Index from "./pages/Index";
import BookPreview from "./pages/BookPreview";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<BookOverview />} />
          <Route path="/dashboard" element={<Index />} />
          <Route path="/chapters" element={<ChaptersOverview />} />
          <Route path="/chapter/:chapterId" element={<ChapterDetail />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/preview" element={<BookPreview />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
