#!/usr/bin/env python3
"""
Reddit User Persona Generator
Main execution script for generating user personas from Reddit profiles.
"""

import argparse
import sys
import os
from typing import Optional

from src.reddit_scraper import RedditScraper
from src.persona_analyzer import PersonaAnalyzer
from src.persona_generator import PersonaGenerator
from src.utils import setup_logging, validate_reddit_url, create_output_directories


def main():
    """Main function to orchestrate the persona generation process."""
    parser = argparse.ArgumentParser(
        description='Generate user persona from Reddit profile'
    )
    parser.add_argument(
        'reddit_url',
        help='Reddit user profile URL (e.g., https://www.reddit.com/user/username/)'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for persona files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    # Validate input
    if not validate_reddit_url(args.reddit_url):
        logger.error("Invalid Reddit URL format")
        sys.exit(1)
    
    # Create output directories
    create_output_directories(args.output_dir)
    
    try:
        # Extract username from URL
        username = args.reddit_url.split('/')[-2] if args.reddit_url.endswith('/') else args.reddit_url.split('/')[-1]
        logger.info(f"Processing user: {username}")
        
        # Step 1: Scrape Reddit data
        logger.info("Step 1: Scraping Reddit data...")
        scraper = RedditScraper()
        user_data = scraper.scrape_user_data(username)
        
        if not user_data['posts'] and not user_data['comments']:
            logger.error("No data found for user. User might be private or non-existent.")
            sys.exit(1)
        
        # Step 2: Analyze content
        logger.info("Step 2: Analyzing content...")
        analyzer = PersonaAnalyzer()
        analysis_results = analyzer.analyze_user_content(user_data)
        
        # Step 3: Generate persona
        logger.info("Step 3: Generating persona...")
        generator = PersonaGenerator()
        persona = generator.generate_persona(analysis_results, user_data)
        
        # Step 4: Save output
        output_file = os.path.join(args.output_dir, f"{username}_persona.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(persona)
        
        logger.info(f"Persona generated successfully: {output_file}")
        
    except Exception as e:
        logger.error(f"Error generating persona: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
