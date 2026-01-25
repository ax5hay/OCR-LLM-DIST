# OCR-LLM Frontend

Beautiful, award-winning Next.js frontend for the OCR-LLM-DIST application featuring real-time chat with streaming responses, document processing, and LMStudio/Ollama integration.

## Features

🎨 **Beautiful UI/UX Design**
- Modern gradient interface with Indigo/Purple color scheme
- Smooth animations and transitions
- Responsive design (mobile, tablet, desktop)
- Dark theme optimized for readability

💬 **Real-time Chat**
- Streaming responses from AI models
- Message history with timestamps
- Beautiful message bubbles with avatars
- Loading states and indicators

📄 **Document Processing**
- PDF and text file upload
- Document context integration
- File preview in chat
- Drag-and-drop support

🤖 **Multi-Backend Support**
- LMStudio integration (default)
- Ollama fallback support
- Backend health monitoring
- Real-time model switching

⚙️ **Advanced Controls**
- Temperature tuning
- Top-P and Top-K parameters
- Model selection dropdown
- Parameter reset functionality

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom React components
- **State Management**: React Hooks
- **API Client**: Axios
- **Notifications**: Sonner
- **Icons**: Lucide React

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+ (for backend)
- LMStudio running on `http://127.0.0.1:1234`
- FastAPI backend running on `http://localhost:8000`

## Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
npm run start
```

## Backend Setup

### 1. Install Python Dependencies

```bash
cd ..
pip install -r requirements.txt
```

### 2. Start FastAPI Server

```bash
python api_server.py
```

The API will be available at `http://localhost:8000`

### 3. Start Streamlit App (Optional)

```bash
streamlit run app.py
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Main chat page
│   │   └── globals.css     # Global styles
│   ├── components/
│   │   ├── ChatInterface.tsx   # Chat messages & input
│   │   └── Sidebar.tsx         # Model/backend selector
│   └── types/
│       └── index.ts        # TypeScript types
├── public/                 # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
└── next.config.js
```

## API Endpoints

The FastAPI backend provides these endpoints:

### Health & Status
- `GET /api/health?backend=lmstudio` - Check backend status
- `GET /api/config` - Get current configuration

### Models
- `GET /api/models?backend=lmstudio` - List available models

### Chat
- `POST /api/chat?message=...&model=...&backend=lmstudio` - Send message with streaming
- `POST /api/upload` - Upload document for context
- `POST /api/clear-context` - Clear conversation context

## Usage

1. **Select Backend**: Choose between LMStudio and Ollama
2. **Choose Model**: Pick from available models
3. **Upload Document** (Optional): Click "Attach" to upload PDF/TXT
4. **Tune Parameters**: Adjust temperature, top-p, top-k in Advanced section
5. **Chat**: Type message and press Send or click the Send button

## Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Customization

### Colors & Theme

Edit `tailwind.config.js` to customize colors:

```js
colors: {
  primary: {
    500: "#6366f1",    // Indigo
    600: "#4f46e5",
    700: "#4338ca",
  },
  purple: {
    500: "#a855f7",    // Purple
    600: "#9333ea",
    700: "#7e22ce",
  },
}
```

### Component Styling

All components use Tailwind CSS classes for easy customization. Edit individual component files in `src/components/`.

## Performance

- **Lazy Loading**: Images and components lazy-loaded
- **Code Splitting**: Automatic with Next.js
- **Streaming**: Server-side streaming for real-time responses
- **Caching**: Optimized cache headers for API responses
- **CSS-in-JS**: Minimal runtime overhead with Tailwind

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android)

## Troubleshooting

### Backend Connection Failed
- Ensure LMStudio is running on `http://127.0.0.1:1234`
- Verify FastAPI server is running on `http://localhost:8000`
- Check firewall settings

### No Models Available
- LMStudio: Install models via UI (http://127.0.0.1:1234)
- Ollama: Run `ollama pull <model>`

### Streaming Timeout
- Increase model's generation timeout
- Check LLM server CPU/memory usage
- Try a smaller model

## Development

### Hot Reload
Changes to files automatically trigger hot reload during development.

### Debugging
Open DevTools (F12) to view console and network logs.

### Building
```bash
npm run build      # Build for production
npm run start      # Start production server
```

## Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/name`
4. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions:
- Check existing GitHub issues
- Create a new issue with detailed description
- Include browser/OS info and error logs

---

Made with ❤️ for beautiful AI interfaces
