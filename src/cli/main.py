import click
import os
from ..models.gemini_handler import GeminiHandler
from ..utils.config import PERSONA_IMAGE_PROMPTS, ERROR_MESSAGES

@click.group()
def cli():
    """Persona Kartı CLI - Generate text and images using Gemini AI."""
    pass

@cli.command()
@click.option('--api-key', envvar='GEMINI_API_KEY', help='Gemini API key')
@click.option('--prompt', help='Text prompt for generation')
@click.option('--temperature', default=0.95, help='Temperature for text generation')
def generate_text(api_key, prompt, temperature):
    """Generate text using Gemini Pro."""
    if not api_key:
        click.echo(ERROR_MESSAGES["api_key_missing"])
        return

    handler = GeminiHandler(api_key)
    result = handler.generate_text(prompt, temperature=temperature)
    
    if result["success"]:
        click.echo(result["response"].text)
    else:
        click.echo(f"Error: {result['error']}")

@cli.command()
@click.option('--api-key', envvar='GEMINI_API_KEY', help='Gemini API key')
@click.option('--persona', type=click.Choice(list(PERSONA_IMAGE_PROMPTS.keys())), help='Persona to generate image for')
@click.option('--custom-prompt', help='Custom prompt for image generation (in English)')
@click.option('--style', type=click.Choice(['Fotoğrafik', 'Çizgi Film', 'Yağlı Boya']), default='Fotoğrafik', help='Style for the generated image')
@click.option('--output', help='Output file path for the generated image')
def generate_image(api_key, persona, custom_prompt, style, output):
    """Generate image using Imagen 3."""
    if not api_key:
        click.echo(ERROR_MESSAGES["api_key_missing"])
        return

    if not persona and not custom_prompt:
        click.echo("Either --persona or --custom-prompt must be provided")
        return

    prompt = custom_prompt if custom_prompt else PERSONA_IMAGE_PROMPTS[persona]
    
    handler = GeminiHandler(api_key)
    result = handler.generate_image(prompt, style)
    
    if result["success"]:
        if output:
            # Save the image to file
            import base64
            image_data = base64.b64decode(result["image_url"].split(',')[1])
            with open(output, 'wb') as f:
                f.write(image_data)
            click.echo(f"Image saved to {output}")
        else:
            click.echo("Image generated successfully. Use --output to save the image.")
    else:
        click.echo(f"Error: {result['error']}")

if __name__ == '__main__':
    cli() 