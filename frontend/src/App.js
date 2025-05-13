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

    /** Network's node data */
    const [node_data, setNodes] = useState(undefined);
    /** Network's Edge data */
    const [edge_data, setEdges] = useState(undefined);
    /** 
     * 'searchQuery' is the query searched in the querybar
     * 'query' is the query sent to Neo4j
     * The querybar value is stored in 'searchQuery', and the true
     * query sent to Neo4j is stored in 'query'. 'query' is not
     * set to 'searchQuery' until the user clicks the "Run Query" button.
     * This way, the query won't change between layouts or while typing!
    */
    const [searchQuery, setSearchQuery] = useState("");
    const [query, setQuery] = useState("GET_EVERYTHING");

    // const [UI, setUI] = useState(false);
    const handleAppendQuery = (text) => {
        setSearchQuery(prevQuery => prevQuery + text);
    };
    /**
     * Similar to subset size! I just added this for a cool demo for Tuesday,
     * however we will need to change this once we componentize everything!
     */
    const [subsetInputSize, setSubsetInputSize] = useState("");
    const [subsetSize, setSubsetSize] = useState("");
    /** Graph layout */
    const [layout, setLayout] = useState("random");
    const handleLayoutChange = (event) => {
        setLayout(event.target.value);
        setNodes(undefined);
    };

    const [queryOption, setQueryOption] = useState(null)
    const handleQueryOption = (event) => {
        setQueryOption(event.target.value)
    }


  // Exxample query to get the number of nodes: MATCH(n) RETURN Count(n) AS nodeCount
  const handleQueryChange = (event) => {
    setSearchQuery(event.target.value);
  }

  // Exxample query to get the number of nodes: MATCH(n) RETURN Count(n) AS nodeCount
  const handleSubsetSizeChange = (event) => {
    setSubsetInputSize(event.target.value);
  }

  useEffect(() => {
    var args = `${layout}/${query}`
    if (subsetSize !== "") {
      if (query !== "") {
        args += "/" + subsetSize;
      } else {
        args += "GET_EVERYTHING" + "/" + subsetSize;
      }
    }
    fetch(`http://127.0.0.1:5000//getlayout/${args}`)
      .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then((data) => {
        console.log(query);
        setNodes(data[0]);
        setEdges(data[1]);
      })
      .catch(error =>
        console.error('There has been a problem with your fetch operation:', error)
      );
  }, [layout, query, subsetSize]);

    if (node_data !== undefined) {
        const node_layer = new ScatterplotLayer({
            id: layout,
            data: node_data,
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
                <div>
                    <button onClick={() => setQueryOption("manual")}>Manual</button>
                    <button onClick={() => setQueryOption("assisted")}>Assisted</button>
                </div>
                {queryOption === "assisted" ? (
                    <div>
                    <div className="query-buttons">
                        <button onClick={() => handleAppendQuery('MATCH (n) ')}>MATCH (n) </button>
                        <button onClick={() => handleAppendQuery('RETURN n.id AS source, m.id AS target ')}>RETURN nodes</button>
                        <button onClick={() => handleAppendQuery('WHERE n.property = "value" ')}>WHERE clause</button>
                        {/*<button onClick={() => handleAppendQuery('LIMIT 10')}>LIMIT 10</button>*/}
                        <button onClick={() => handleAppendQuery('MATCH (n)-[r]->(m) ')}>MATCH relationships</button>
                        <button onClick={() => setQuery("GET_EVERYTHING")}>GET EVERYTHING</button>
                    </div>
                    <input
                        type="text"
                        placeholder="Subset Size"
                        className="p-2 border rounded bg-black text-white shadow w-32"
                        value={subsetInputSize}
                        onChange={(e) => handleSubsetSizeChange(e)}
                    />
                    <button onClick={() => setSubsetSize(subsetInputSize)}>Visualize Subset</button>
                </div>) : queryOption === "manual" ? (
                    <div></div>
                ) : (<p>Please select a mode (Manual or Assisted) to get started.</p>)}
                <input
                    type="text"
                    placeholder="Query"
                    className="p-2 border rounded bg-black text-white shadow w-32"
                    value={searchQuery}
                    onChange={(e) => handleQueryChange(e)}
                />
                <button onClick={() => setQuery(searchQuery)}>Run Query</button>
                <button onClick={() => setSearchQuery("")}>Clear Query Search</button>
                
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
    } 
    else if (edge_data){
        /** While we're waiting for the Flask call */
        return <p>Rerendering with new layout...</p>
    } 
    else {
        return <p>Loading...</p>;
    }

  }