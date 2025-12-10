import { useState, useEffect, useRef } from 'react'
import Editor from '@monaco-editor/react'
import axios from 'axios'
import html2canvas from 'html2canvas'
import './App.css'

function App() {
  const [markdown, setMarkdown] = useState<string>('# Hello World\n\nType some markdown here...')
  const [html, setHtml] = useState<string>('')
  const [themes, setThemes] = useState<string[]>([])
  const [selectedTheme, setSelectedTheme] = useState<string>('default_config')
  const previewRef = useRef<HTMLDivElement>(null)

  const [isExporting, setIsExporting] = useState<boolean>(false)

  useEffect(() => {
    fetchThemes()
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => {
      renderMarkdown()
    }, 500)
    return () => clearTimeout(timer)
  }, [markdown, selectedTheme])

  const fetchThemes = async () => {
    try {
      const res = await axios.get('/api/themes')
      setThemes(res.data.themes)
      // Try to pick a better default theme than 'default_config'
      if (res.data.themes.length > 0) {
        if (!res.data.themes.includes(selectedTheme) || selectedTheme === 'default_config') {
             const betterTheme = res.data.themes.find((t: string) => t !== 'default_config') || res.data.themes[0]
             setSelectedTheme(betterTheme)
        }
      }
    } catch (err) {
      console.error(err)
    }
  }

  const renderMarkdown = async () => {
    try {
      const res = await axios.post('/api/render', {
        markdown,
        theme: selectedTheme
      })
      setHtml(res.data.html)
    } catch (err) {
      console.error(err)
    }
  }

  const copyToClipboard = () => {
    if (previewRef.current) {
        // We need to copy the innerHTML but plain text fallback is needed.
        const content = previewRef.current.innerHTML;
        const textContent = previewRef.current.innerText;
        
        const blobHtml = new Blob([content], { type: 'text/html' });
        const blobText = new Blob([textContent], { type: 'text/plain' });
        
        try {
            const item = new ClipboardItem({
                'text/html': blobHtml,
                'text/plain': blobText
            });
            navigator.clipboard.write([item]).then(() => {
                alert('已复制到剪贴板，可直接粘贴到微信公众号')
            })
        } catch (err) {
            console.error(err)
            // Fallback for older browsers or insecure contexts (though API requires secure context)
            alert('复制失败，可能是浏览器权限问题')
        }
    }
  }

  const exportImage = async () => {
    if (previewRef.current && !isExporting) {
        setIsExporting(true)
        
        // Use setTimeout to allow UI to update (show loading state)
        await new Promise(resolve => setTimeout(resolve, 100));

        try {
            // 1. Create a temporary container for mobile rendering (Off-screen)
            const container = document.createElement('div');
            container.style.position = 'absolute';
            container.style.left = '-9999px';
            container.style.top = '0';
            container.style.width = '375px'; // Fixed mobile width
            container.style.backgroundColor = '#fff';
            container.style.zIndex = '-1';
            
            // 2. Clone content
            // We wrap it in a div that matches preview-content class to inherit basic styles
            const contentClone = document.createElement('div');
            contentClone.className = 'preview-content';
            contentClone.innerHTML = previewRef.current.innerHTML;
            
            // 3. Override styles for mobile export
            // These inline styles will override CSS class styles
            contentClone.style.width = '100%';
            contentClone.style.maxWidth = 'none';
            contentClone.style.height = 'auto';
            contentClone.style.minHeight = 'auto';
            contentClone.style.padding = '20px 15px'; // Mobile padding
            contentClone.style.margin = '0';
            contentClone.style.boxShadow = 'none';
            contentClone.style.overflow = 'visible'; // Ensure full height is visible
            
            // 4. Append to body to trigger layout calculation
            container.appendChild(contentClone);
            document.body.appendChild(container);

            // 5. Capture using html2canvas
            // We capture the 'container' which is constrained to 375px
            const canvas = await html2canvas(container, {
                useCORS: true,
                scale: 3, // High resolution (3x)
                backgroundColor: '#ffffff',
                windowWidth: 375,
                height: container.scrollHeight, // Capture full height
                onclone: (doc) => {
                     // Ensure images in the clone are loaded/styled correctly
                     const images = doc.querySelectorAll('.preview-content img');
                     images.forEach((img) => {
                        (img as HTMLElement).style.maxWidth = '100%';
                        (img as HTMLElement).style.height = 'auto';
                     });
                }
            });
            
            // 6. Download
            const url = canvas.toDataURL("image/png");
            const a = document.createElement("a");
            a.href = url;
            a.download = "article_mobile.png";
            a.click();
            
            // 7. Cleanup
            document.body.removeChild(container);
            
        } catch (e) {
            console.error(e)
            alert("导出图片失败")
        } finally {
            setIsExporting(false)
        }
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>HZWZ Markdown Editor</h1>
        <select value={selectedTheme} onChange={e => setSelectedTheme(e.target.value)}>
          {themes.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <button onClick={copyToClipboard}>复制到公众号</button>
        <button onClick={exportImage} disabled={isExporting}>
            {isExporting ? '导出中...' : '导出长图'}
        </button>
      </div>
      <div className="main">
        <div className="editor-pane">
          <Editor 
            height="100%" 
            defaultLanguage="markdown" 
            value={markdown}
            onChange={(value) => setMarkdown(value || '')}
            theme="vs-dark"
            options={{
                minimap: { enabled: false },
                wordWrap: 'on'
            }}
          />
        </div>
        <div className="preview-pane">
          <div 
            ref={previewRef}
            className="preview-content"
            dangerouslySetInnerHTML={{ __html: html }} 
          />
        </div>
      </div>
    </div>
  )
}

export default App
