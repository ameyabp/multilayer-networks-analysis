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
    const [layout, setLayout] = useState<string>("graph_layout_circular.csv");
    const handleLayoutChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setLayout(event.target.value);
    };

    useEffect(() => {
        fetch(`/igraph_generated_layouts/${layout}`)
        .then(response => {
            if (!response.ok) throw new Error('Network error');
            return response.text();
        })
        .then(csvText => {
            const result = Papa.parse<NodeData>(csvText, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
            });
            setNodes(result.data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    }, [layout]);

    if (data !== undefined) {
        const layer = new ScatterplotLayer({
        id: 'scatterplot-layer',
        data,
        getPosition: d => [d.Long1, d.Lat1],
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
                <option value="graph_layout_circular.csv">Circular</option>
                <option value="graph_layout_fr.csv">Fruchterman-Reingold</option>
                <option value="graph_layout_random.csv">Random</option>
                <option value="graph_layout_star.csv">Star</option>
            </select>
            </div>

            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={true}
                layers={[layer]}
            />
        </div>
        );
    } else {
        return <p>Loading...</p>;
    }
}
