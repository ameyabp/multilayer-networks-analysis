"use client";

import { DeckGL } from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';
import { useState, useEffect } from 'react';
import * as Papa from 'papaparse';

type NodeData = {
    Node: number;
    Long1: number;
    Lat1: number;
};

const INITIAL_VIEW_STATE = {
    longitude: 0,
    latitude: 0,
    zoom: 5,
    pitch: 0,
    bearing: 0
};

export default function Home() {
    const [data, setNodes] = useState<NodeData[] | undefined>(undefined);
    const [layout, setLayout] = useState<string>("circular");
    const handleLayoutChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setLayout(event.target.value);
    };

  const [search, setSearch] = useState<string>("");

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/${layout}`)
      .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then((data: NodeData[]) => {
        setNodes(data);
      })
      .catch(error =>
        console.error('There has been a problem with your fetch operation:', error)
      );
  }, [layout]);

    if (data !== undefined) {
        /*TEMPORARY PLACEHOLDER*/
        const filteredData = data.filter(d => {
            if (!search.trim()) return true;
            return d.Node.toString().includes(search.trim());
        });

        
        const layer = new ScatterplotLayer({
            id: layout,
            data: filteredData, // temporary
            getPosition: d => [d[1], d[2]],
            getFillColor: [255, 0, 0],
            getRadius: 100,
            radiusMinPixels: 5,
        });

        return (
        <div>
            <div className="absolute top-4 right-4 z-50">
                <select
                    className="p-2 border rounded bg-black text-white shadow"
                    value={layout}
                    onChange={handleLayoutChange}
                >
                    <option value="circular">Circular</option>
                    <option value="fruchterman_reingold">Fruchterman-Reingold</option>
                    <option value="random">Random</option>
                    <option value="star">Star</option>
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
                layers={[layer]}
                key={layout}
            />
        </div>
        );
    } else {
        return <p>Loading...</p>;
    }

}
