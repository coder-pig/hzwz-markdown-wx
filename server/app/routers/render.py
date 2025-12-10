from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..core.themes import get_all_themes, get_theme
from ..core.renderer import render_article

router = APIRouter()

class RenderRequest(BaseModel):
    markdown: str
    theme: str = "default_config"

@router.get("/themes")
async def list_themes():
    return {"themes": get_all_themes()}

@router.post("/render")
async def render_markdown(request: RenderRequest):
    theme_data = get_theme(request.theme)
    if not theme_data:
        # Try finding a theme that matches partially or just fallback
        # User might pass "default_config" but file is "default_config.ini" -> id is "default_config"
        # If not found, check if "default_config" exists
        if "default_config" in get_all_themes():
            theme_data = get_theme("default_config")
        else:
            # Pick the first available one
            all_themes = get_all_themes()
            if all_themes:
                theme_data = get_theme(all_themes[0])
            else:
                raise HTTPException(status_code=500, detail="No themes available")
    
    try:
        html_content = render_article(request.markdown, theme_data)
        return {"html": html_content}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
