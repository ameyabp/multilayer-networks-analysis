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
    fetch('http://127.0.0.1:5000/')
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
  }, []);

  if (data !== undefined) {
    console.log(data)
    const layer = new ScatterplotLayer({
      id: 'scatterplot-layer',
      data,
      getPosition: d => [d[1], d[2]],
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
