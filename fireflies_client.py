#!/usr/bin/env python3
"""
Fireflies.ai API Client for downloading meeting transcripts as markdown files.
This module fetches the last 10 meetings and saves their transcripts in markdown format.
"""

import os
import json
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FirefliesClient:
    """Client for interacting with Fireflies.ai GraphQL API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Fireflies client.
        
        Args:
            api_key: Fireflies API key. If None, will try to load from environment.
        """
        self.api_key = api_key or os.getenv('FIREFLIES_API_KEY')
        if not self.api_key:
            raise ValueError("Fireflies API key is required. Set FIREFLIES_API_KEY environment variable.")
        
        self.base_url = "https://api.fireflies.ai/graphql"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
    async def _make_request(self, query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a GraphQL request to the Fireflies API.
        
        Args:
            query: GraphQL query string
            variables: Optional variables for the query
            
        Returns:
            Response data from the API
        """
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, 
                                      json=payload, 
                                      headers=self.headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if 'errors' in data:
                        raise Exception(f"GraphQL errors: {data['errors']}")
                    
                    return data['data']
                    
            except aiohttp.ClientError as e:
                raise Exception(f"API request failed: {str(e)}")

    async def get_meetings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch the last N meetings.
        
        Args:
            limit: Number of meetings to fetch (default: 10)
            
        Returns:
            List of meeting objects with basic information
        """
        query = """
        query GetMeetings {
            transcripts {
                id
                title
                date
                dateString
                duration
                host_email
                organizer_email
                participants
                transcript_url
                audio_url
                video_url
                privacy
                calendar_type
                user {
                    name
                    email
                }
            }
        }
        """
        
        try:
            data = await self._make_request(query)
            meetings = data.get('transcripts', [])
            
            # Sort by date (most recent first) and limit results
            meetings_sorted = sorted(meetings, key=lambda x: x.get('date', 0), reverse=True)
            return meetings_sorted[:limit]
            
        except Exception as e:
            print(f"Error fetching meetings: {str(e)}")
            return []

    async def get_transcript_detail(self, transcript_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed transcript data for a specific meeting.
        
        Args:
            transcript_id: ID of the transcript to fetch
            
        Returns:
            Detailed transcript data including sentences, speakers, and summary
        """
        query = """
        query GetTranscriptDetail($transcriptId: String!) {
            transcript(id: $transcriptId) {
                id
                title
                dateString
                date
                duration
                privacy
                host_email
                organizer_email
                participants
                transcript_url
                audio_url
                video_url
                calendar_type
                speakers {
                    id
                    name
                }
                sentences {
                    index
                    speaker_name
                    speaker_id
                    text
                    raw_text
                    start_time
                    end_time
                }
                summary {
                    keywords
                    action_items
                    outline
                    shorthand_bullet
                    overview
                    bullet_gist
                    gist
                    short_summary
                    meeting_type
                    topics_discussed
                }
                analytics {
                    sentiments {
                        negative_pct
                        neutral_pct
                        positive_pct
                    }
                    speakers {
                        speaker_id
                        name
                        duration
                        word_count
                        duration_pct
                        words_per_minute
                    }
                }
                meeting_attendees {
                    displayName
                    email
                    phoneNumber
                    name
                    location
                }
                user {
                    user_id
                    email
                    name
                }
            }
        }
        """
        
        try:
            data = await self._make_request(query, {'transcriptId': transcript_id})
            return data.get('transcript')
            
        except Exception as e:
            print(f"Error fetching transcript {transcript_id}: {str(e)}")
            return None

    def format_transcript_as_markdown(self, transcript: Dict[str, Any]) -> str:
        """
        Convert transcript data to markdown format.
        
        Args:
            transcript: Transcript data from API
            
        Returns:
            Formatted markdown string
        """
        if not transcript:
            return "# Error: No transcript data available\n"
        
        # Clean title for filename safety
        title = transcript.get('title', 'Untitled Meeting')
        date_str = transcript.get('dateString', 'Unknown Date')
        duration = transcript.get('duration', 0)
        duration_formatted = f"{duration // 60}m {duration % 60}s" if duration else "Unknown"
        
        markdown = f"""# {title}

**Date:** {date_str}  
**Duration:** {duration_formatted}  
**Host:** {transcript.get('host_email', 'Unknown')}  
**Organizer:** {transcript.get('organizer_email', 'Unknown')}  
**Meeting Type:** {transcript.get('summary', {}).get('meeting_type', 'Unknown')}

"""
        
        # Add participants
        participants = transcript.get('participants', [])
        if participants:
            markdown += "**Participants:**\n"
            for participant in participants:
                markdown += f"- {participant}\n"
            markdown += "\n"
        
        # Add summary if available
        summary = transcript.get('summary', {})
        if summary:
            markdown += "## Meeting Summary\n\n"
            
            if summary.get('overview'):
                markdown += f"**Overview:** {summary['overview']}\n\n"
            
            if summary.get('topics_discussed'):
                markdown += "**Topics Discussed:**\n"
                topics = summary['topics_discussed']
                if isinstance(topics, list):
                    for topic in topics:
                        markdown += f"- {topic}\n"
                else:
                    markdown += f"{topics}\n"
                markdown += "\n"
            
            if summary.get('action_items'):
                markdown += "**Action Items:**\n"
                actions = summary['action_items']
                if isinstance(actions, list):
                    for action in actions:
                        markdown += f"- {action}\n"
                else:
                    markdown += f"{actions}\n"
                markdown += "\n"
            
            if summary.get('keywords'):
                markdown += f"**Keywords:** {', '.join(summary['keywords']) if isinstance(summary['keywords'], list) else summary['keywords']}\n\n"
        
        # Add speaker analytics if available
        analytics = transcript.get('analytics', {})
        if analytics and analytics.get('speakers'):
            markdown += "## Speaker Analytics\n\n"
            for speaker in analytics['speakers']:
                name = speaker.get('name', 'Unknown Speaker')
                duration_pct = speaker.get('duration_pct', 0)
                word_count = speaker.get('word_count', 0)
                wpm = speaker.get('words_per_minute', 0)
                markdown += f"**{name}:** {duration_pct:.1f}% talk time, {word_count} words, {wpm:.1f} WPM\n"
            markdown += "\n"
        
        # Add sentiment analysis if available
        if analytics and analytics.get('sentiments'):
            sentiments = analytics['sentiments']
            markdown += "## Sentiment Analysis\n\n"
            markdown += f"- Positive: {sentiments.get('positive_pct', 0):.1f}%\n"
            markdown += f"- Neutral: {sentiments.get('neutral_pct', 0):.1f}%\n"
            markdown += f"- Negative: {sentiments.get('negative_pct', 0):.1f}%\n\n"
        
        # Add full transcript
        sentences = transcript.get('sentences', [])
        if sentences:
            markdown += "## Full Transcript\n\n"
            
            current_speaker = None
            for sentence in sentences:
                speaker_name = sentence.get('speaker_name', 'Unknown Speaker')
                text = sentence.get('text', sentence.get('raw_text', ''))
                start_time = sentence.get('start_time', 0)
                
                # Format timestamp
                minutes = int(start_time // 60)
                seconds = int(start_time % 60)
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                
                # Group consecutive sentences by same speaker
                if speaker_name != current_speaker:
                    if current_speaker is not None:
                        markdown += "\n"
                    markdown += f"**{speaker_name}** {timestamp}\n\n"
                    current_speaker = speaker_name
                
                markdown += f"{text} "
            
            markdown += "\n"
        
        # Add metadata footer
        markdown += "\n---\n\n"
        markdown += f"**Transcript ID:** {transcript.get('id', 'Unknown')}\n"
        if transcript.get('transcript_url'):
            markdown += f"**Original URL:** {transcript['transcript_url']}\n"
        if transcript.get('audio_url'):
            markdown += f"**Audio URL:** {transcript['audio_url']}\n"
        if transcript.get('video_url'):
            markdown += f"**Video URL:** {transcript['video_url']}\n"
        
        return markdown

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to be safe for filesystem.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace problematic characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[^\w\s\-_.]', '', filename)
        filename = re.sub(r'\s+', '_', filename)
        filename = filename.strip('._')
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename or "untitled_meeting"

    async def download_transcripts(self, output_dir: str = "fireflies_transcripts", limit: int = 10):
        """
        Download the last N meeting transcripts as markdown files.
        
        Args:
            output_dir: Directory to save transcripts (default: "fireflies_transcripts")
            limit: Number of transcripts to download (default: 10)
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"Fetching last {limit} meetings from Fireflies...")
        
        # Get list of meetings
        meetings = await self.get_meetings(limit)
        
        if not meetings:
            print("No meetings found.")
            return
        
        print(f"Found {len(meetings)} meetings. Downloading transcripts...")
        
        # Download each transcript
        for i, meeting in enumerate(meetings, 1):
            meeting_id = meeting.get('id')
            title = meeting.get('title', 'Untitled Meeting')
            date_str = meeting.get('dateString', 'Unknown Date')
            
            print(f"[{i}/{len(meetings)}] Processing: {title} ({date_str})")
            
            try:
                # Get detailed transcript
                transcript = await self.get_transcript_detail(meeting_id)
                
                if transcript:
                    # Convert to markdown
                    markdown_content = self.format_transcript_as_markdown(transcript)
                    
                    # Create filename
                    safe_title = self.sanitize_filename(title)
                    safe_date = self.sanitize_filename(date_str)
                    filename = f"{safe_date}_{safe_title}.md"
                    
                    # Save to file
                    file_path = output_path / filename
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    print(f"✓ Saved: {filename}")
                else:
                    print(f"✗ Failed to download transcript for: {title} (No data returned)")
                    
            except Exception as e:
                print(f"✗ Error processing {title}: {str(e)}")
                # Continue with next meeting instead of crashing
                continue
            
            # Small delay to be respectful to API
            await asyncio.sleep(0.5)
        
        print(f"\nCompleted! Transcripts saved in: {output_path.absolute()}")


async def main():
    """Main function to download transcripts."""
    try:
        # Initialize client
        client = FirefliesClient()
        
        # Download last 10 transcripts
        await client.download_transcripts(limit=10)
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())