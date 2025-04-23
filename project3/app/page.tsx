"use client";

import { DeckGL } from '@deck.gl/react';
import { ScatterplotLayer, LineLayer } from '@deck.gl/layers';
import { useState, useEffect } from 'react';
import * as Papa from 'papaparse';

type NodeData = {
    Node: number;
    Long1: number;
    Lat1: number;
};

type EdgeData = {
    Edge: number;
    FromCoordinates: [number, number];
    ToCoordinates: [number, number];
};

const INITIAL_VIEW_STATE = {
    longitude: 0,
    latitude: 0,
    zoom: 5,
    pitch: 0,
    bearing: 0
};

export default function Home() {
    const [node_data, setNodes] = useState<NodeData[] | undefined>(undefined);
    const [edge_data, setEdges] = useState<EdgeData[] | undefined>(undefined);
    const [layout, setLayout] = useState<string>("random");
    const handleLayoutChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setLayout(event.target.value);
        setNodes(undefined);
    };

  const [search, setSearch] = useState<string>("");

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/${layout}`)
      .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then((data: ([NodeData[], EdgeData[]])) => {
        setNodes(data[0]);
        console.log(data[1]);
        setEdges(data[1]);
      })
      .catch(error =>
        console.error('There has been a problem with your fetch operation:', error)
      );
  }, [layout]);

    if (node_data !== undefined) {
        /*TEMPORARY PLACEHOLDER*/
        const filteredData = node_data.filter(d => {
            if (!search.trim()) return true;
            return d.Node.toString().includes(search.trim());
        });

        
        const node_layer = new ScatterplotLayer({
            id: layout,
            data: filteredData, // temporary
            getPosition: d => [d[1], d[2]],
            getFillColor: [255, 0, 0],
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
            <div className="absolute top-4 right-4 z-50">
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
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>

            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={[edge_layer, node_layer]}
                key={layout}
            />
        </div>
        );
    } else if (edge_data){
        return <p>Rerendering with new layout...</p>
    } else {
        return <p>Loading...</p>;
    }

}
