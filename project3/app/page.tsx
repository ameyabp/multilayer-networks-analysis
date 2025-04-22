"use client";

import { DeckGL } from '@deck.gl/react';
import { ScatterplotLayer, _TextBackgroundLayer } from '@deck.gl/layers';
import { useState,useEffect } from 'react';
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

  useEffect(() => {
    fetch('/igraph_generated_layouts/graph_layout_random.csv')
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
      .catch(error =>
        console.error('There has been a problem with your fetch operation:', error)
      );
  }, []); 

  if (data !== undefined) {
    const layer = new ScatterplotLayer({
      id: 'scatterplot-layer',
      data,
      getPosition: d => [d.Long1, d.Lat1],
      getFillColor: [255, 0,0],
      getRadius: 100,
      radiusMinPixels: 5,
    });
    console.log(layer);
    return (
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        layers= {[layer]}
      />
    );
  } else {
    return <p>loading...</p>;
  }
  
}
