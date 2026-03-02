#!/usr/bin/env python3
"""
Silver-hand v3.0 CLI - AI-Powered Pentest Framework
Developer: SayerLinux | SayerLinux1@gmail.com
"""
import click
import asyncio
from rich.console import Console
from rich.panel import Panel
from silverhand.engine import SilverHandEngineV3
from silverhand.ai.chat import AIChatAssistant
from silverhand.themes.blue import apply_blue_theme

console = Console()
apply_blue_theme(console)

@click.group()
@click.option('--target', '-t', help='Target URL/Domain')
@click.option('--dangerous', is_flag=True, help='[REQUIRED] Enable PoC execution')
@click.option('--ai', is_flag=True, help='Enable AI Assistant (Unmonitored)')
@click.pass_context
def silverhand(ctx, target, dangerous, ai):
    """🌊 Silver-hand v3.0 - AI-Powered Ultimate Pentest"""
    console.print(Panel.fit(
        "[bold magenta]🤖 SILVER-HAND v3.0 AI ULTIMATE ACTIVATED 🤖[/bold magenta]\n"
        "[bold cyan]Developer:[/bold cyan] SayerLinux | [link]SayerLinux1@gmail.com[/link]\n"
        "[bold yellow]🚀 AI Chat | Zero-Day Hunter | Unmonitored Local LLM[/bold yellow]",
        title="[bold magenta]Silver-hand AI v3.0[/bold magenta]", 
        border_style="bright_magenta"
    ))
    
    ctx.obj = {
        'target': target,
        'dangerous': dangerous,
        'ai_enabled': ai,
        'ai_assistant': AIChatAssistant() if ai else None
    }

@silverhand.command()
@click.pass_context
def ai_chat(ctx):
    """🤖 AI Pentest Assistant (Unmonitored Local Chat)"""
    if ctx.obj['ai_enabled'] and ctx.obj['ai_assistant']:
        console.print("[bold green]🤖 AI Assistant Online - Unmonitored Local Session[/bold green]")
        asyncio.run(ctx.obj['ai_assistant'].start_chat_session())
    else:
        console.print("[red]❌ AI mode disabled. Use --ai flag[/red]")

@silverhand.command()
@click.pass_context
def ultimate(ctx):
    """⚡ ULTIMATE AI-Guided Full Assessment"""
    engine = SilverHandEngineV3(ctx.obj['target'], ctx.obj['dangerous'])
    ai = ctx.obj.get('ai_assistant')
    
    results = asyncio.run(engine.ultimate_assessment())
    
    if ai:
        analysis = asyncio.run(ai.analyze_results(results))
        console.print(f"[bold yellow]🤖 AI Analysis:[/bold yellow]\n{analysis}")
    
    console.print(f"[bold green]🎉 ULTIMATE COMPLETE: {results['report_path']}[/bold green]")

@silverhand.command()
@click.pass_context
def takeover(ctx):
    """🔒 Subdomain Takeover Detection"""
    engine = SilverHandEngineV3(ctx.obj['target'])
    results = asyncio.run(engine.detect_subdomain_takeovers())
    console.print(f"[magenta]🔒 {len(results)} takeover risks detected[/magenta]")

if __name__ == '__main__':
    silverhand()
