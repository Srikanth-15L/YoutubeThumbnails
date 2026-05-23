YouTube Thumbnailer Agent

 I built this project because generating a great YouTube thumbnail usually takes a ton of trial and error. Instead of manually tweaking prompts over and over, I decided to automate the entire creative loop using LangGraph,GPT-4o and DALL-E .


This is an autonomous, self-improving AI agent. You give it a topic (e.g., "why Python is the best language"), and it doesn't just generate a single image and call it a day. Instead, it enters a critical feedback loop:

 Web Search**: It searches the web (via Tavily) for context on the topic.
 Prompt Writer**: It drafts a highly optimized prompt for DALL-E.
 Generator**: It calls DALL-E 3 to actually generate the image.
 Critic (The Secret Sauce)**: A Vision LLM looks at the generated image, rates it on a scale of 1-10, and provides *actionable critique*.

If the rating is below the target (e.g., 9/10), the agent **loops back** to the Prompt Writer, feeding it the critique so it can fix the issues and try again. 

Once the image hits the target rating (or max iterations are reached), it passes to the  Saver**, which outputs the `final.png` alongside a detailed `report.md` documenting every iteration.
 Architecture
Under the hood, this is a state machine built with **LangGraph**:
1. Define the State (`Thumbnail`)
2. Create the Nodes (Search, Prompt Writer, Generator, Critic, Saver)
3. Add Edges (including the conditional edge that loops the Critic back to the Prompt Writer)
4., Compile & Execute


1. Make sure you have your `.env` file set up with your OpenAI and Tavily API keys.
2. Activate your virtual environment:
   ```bash
   .venv\Scripts\activate
   ```
3. Run the main script:
   ```bash
   python main.py
   ```
4. Check the `outputs/` directory! Every run creates a timestamped folder containing all iteration images, the `report.md`, and your polished `final.png`.


