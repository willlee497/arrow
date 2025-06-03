export default async function handler(req, res) {
  try {
    let { prompt } = req.body;

    // Capitalize first letter of input
    prompt = prompt.charAt(0).toUpperCase() + prompt.slice(1);

    console.log("Prompt being sent:", prompt);
    console.log("API Key starts with:", process.env.OPENAI_API_KEY?.slice(0, 5));

    const fullPrompt = `You are WilliamAI, a voice-interactive assistant representing William Lee. Speak like a confident, friendly candidate who is humble but accomplished. Respond conversationally and convincingly.

If asked "What are your skills?":
Highlight William’s backend, cloud, and AI strengths. Mention Rust, Python, Kubernetes, gRPC, GPT-3.5, AWS/GCP, CI/CD, and real-time systems.

If asked "Why Arrow?":
Mention Arrow’s fast-paced, AI-native environment. Emphasize that William built this real-time LLM voice bot before even being hired, and he thrives in environments that move fast and build smart.

If asked "What have you built?":
Talk about:
- An AI terminal for automating OS tasks using GPT-3.5 and gRPC
- Mortgage and real estate tools using AWS, Puppeteer, and APIs
- ElevateMC, a Minecraft server with 2M+ logins and NPC plugin system
- Legislative insight extraction using LangChain on 65K+ records
- Full-stack invasive fish mapping app using OpenAI, Leaflet.js, and clustering

Always sound energetic, smart, and collaborative. Include details that show initiative, debugging skills, and ability to lead dev teams.`;

    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
        "OpenAI-Project": "proj_FDym5DuHLjuW5MOxQcjC3Odf",
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [
          { role: "system", content: fullPrompt },
          { role: "user", content: prompt }
        ],
        temperature: 0.75,
      }),
    });

    const data = await response.json();

    if (data.choices && data.choices.length > 0) {
      res.status(200).json({ response: data.choices[0].message.content });
    } else {
      console.error("No choices returned from OpenAI:", data);
      res.status(500).json({ response: "Sorry, I couldn't generate a response." });
    }
  } catch (err) {
    console.error("Error generating OpenAI response:", err);
    res.status(500).json({ response: "Error occurred generating response." });
  }
}