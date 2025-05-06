import DeckGL from '@deck.gl/react';
import { ScatterplotLayer, LineLayer } from '@deck.gl/layers';
import { useState, useEffect } from 'react';
import './components.css'
// import * as Papa from 'papaparse';

document.title = 'Project3';

const INITIAL_VIEW_STATE = {
    longitude: 0,
    latitude: 0,
    zoom: 5,
    pitch: 0,
    bearing: 0
};

export default function Home() {
    const [node_data, setNodes] = useState(undefined);
    const [edge_data, setEdges] = useState(undefined);
    const [query, setQuery] = useState("");
    const [queryResults, setQueryResults] = useState("");
    const [layout, setLayout] = useState("random");
    const handleLayoutChange = (event) => {
        setLayout(event.target.value);
        setNodes(undefined);
    };

  // Exxample query to get the number of nodes: MATCH(n) RETURN Count(n) AS nodeCount
  const handleQuertyChange = (event) => {
    console.log(event.target.value);
    fetch(`http://127.0.0.1:5000//query/${event.target.value}/`)
      .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then((data) => {
        console.log(data);
      })
      .catch(error =>
        console.error('There has been a problem with your fetch operation:', error)
      );
  }



  useEffect(() => {
    fetch(`http://127.0.0.1:5000//getlayout/${layout}`)
      .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then((data) => {
        setNodes(data[0]);
        setEdges(data[1]);
      })
      .catch(error =>
        console.error('There has been a problem with your fetch operation:', error)
      );
  }, [layout]);

    if (node_data !== undefined) {
        /*TEMPORARY PLACEHOLDER*/
        const filteredData = node_data //.filter(d => {
        //     if (!query.trim()) return true;
        //     return d.Node.toString().includes(query.trim());
        // });


        const node_layer = new ScatterplotLayer({
            id: layout,
            data: filteredData, // temporary
            getPosition: d => [d[1], d[2]],
            getFillColor: [255, 0, 0],
            pickable: true,
            autoHighlight: true,
            highlightColor: [0, 255, 0],
            getRadius: 100,
            radiusMinPixels: 5,
        });

        const edge_layer = new LineLayer({
            id: 'LineLayer',
            data: edge_data,
            getColor: d => [0, 0, 255],
            getSourcePosition: d => d[0],
            getTargetPosition: d => d[1],
            getWidth: 1,
            pickable: true
          });

        return (
        <div>
            <div className="Select">
                <select
                    className="p-2 border rounded bg-black text-white shadow"
                    value={layout}
                    onChange={handleLayoutChange}
                >
                    <option value="random">Random</option>
                    <option value="circle">Circle</option>
                    <option value="fruchterman_reingold">Fruchterman-Reingold</option>
                    <option value="star">Star</option>
                    <option value="grid">Grid</option>
                    <option value="drl">Drl</option>
                    <option value="kamada_kawai">Kamada Kawai</option>
                    <option value="graphopt">Graphopt</option>
                    <option value="davidson_harel">Davidson Harel</option>
                    <option value="sugiyama">Sugiyama</option>
                </select>

                {/*TEMPORARY PLACEHOLDER*/}
                <input
                    type="text"
                    placeholder="Query"
                    className="p-2 border rounded bg-black text-white shadow w-32"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button onClick={handleQuertyChange} value={query}>Search!</button>
                <p>{queryResults}</p>
            </div>
            <div className="DeckGL">
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={[edge_layer, node_layer]}
                key={layout}
            />
            </div>
        </div>
        );
    } else if (edge_data){
        /** While we're waiting for the Flask call */
        return <p>Rerendering with new layout...</p>
    } else {
        return <p>Loading...</p>;
    }

}
