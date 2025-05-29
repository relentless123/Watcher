def generate_browser_task(url: str) -> str:
    """Generate the browser task prompt for performing Content moderation"""
    return f"""Please go to the URL {url} and analyze its content
for adherence to Google's content moderation policies. 
If any content violates these policies, list the problematic sections or 
elements and provide a clear, concise reason for flagging each one. 
Ensure your evaluation covers all aspects of Google's content model,
including but not limited to: hate speech, violence, sexually explicit material,
harassment, dangerous content, illegal activities, spam, and misrepresentation.

**Output Format:**

```json
{{
  "problematic_content": [
    {{
      "item": "[Excerpt of problematic content or description of problematic element]",
      "reason": "[Specific Google content policy violation, e.g., 'Hate Speech - targets a protected group based on religion']"
    }}
    // Add more objects if multiple issues are found
  ]
}}
```

**URL:** {url}"""