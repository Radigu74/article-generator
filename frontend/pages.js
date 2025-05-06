import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [keywords, setKeywords] = useState("");
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");
  const [article, setArticle] = useState("");
  const [tone, setTone] = useState("Informative");

  const API = "https://<YOUR_BACKEND>/api";
  const headers = { "X-API-KEY": "CLIENT_SPECIFIC_KEY" };

  const genTopics = async () => {
    const { data } = await axios.post(
      `${API}/topics`,
      { keywords, num_topics: 7 },
      { headers }
    );
    setTopics(data.topics.split("\n\n"));
  };

  const genArticle = async () => {
    const { data } = await axios.post(
      `${API}/articles`,
      { topic: selectedTopic, tone, length: 200 },
      { headers }
    );
    setArticle(data.article);
  };

  return (
    <div className="flex h-screen">
      {/* Left: Topic Generator */}
      <div className="w-1/2 p-4">
        <h2>Generate Topics</h2>
        <input
          value={keywords}
          onChange={e => setKeywords(e.target.value)}
          placeholder="Enter keywords"
          className="border p-2 w-full"
        />
        <button onClick={genTopics} className="mt-2 bg-blue-600 text-white px-4 py-2">
          Generate
        </button>
        <ul className="mt-4">
          {topics.map((t,i) => (
            <li
              key={i}
              onClick={()=> setSelectedTopic(t)}
              className={`cursor-pointer p-2 ${t===selectedTopic?"bg-blue-100":""}`}
            >{t}</li>
          ))}
        </ul>
      </div>

      {/* Right: Article Generator */}
      <div className="w-1/2 p-4">
        <h2>Generate Article</h2>
        <div className="mb-2">
          <label>Tone:</label>
          <select value={tone} onChange={e=>setTone(e.target.value)} className="border p-1 ml-2">
            {["Informative","Professional","Engaging","Entertaining"].map(t=>(
              <option key={t}>{t}</option>
            ))}
          </select>
        </div>
        <button onClick={genArticle} className="bg-green-600 text-white px-4 py-2">
          Generate
        </button>
        <textarea
          value={article}
          readOnly
          rows={10}
          className="mt-4 border p-2 w-full"
        />
      </div>
    </div>
  );
}
