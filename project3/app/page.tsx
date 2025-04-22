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
  zoom: 3,
};

export default function Home() {
  const [nodes, setNodes] = useState<NodeData[] | null>(null);
  const data = [
  {Long1: -123.4, Lat1: 37.8, color: [0, 0, 255] }
];
console.log(data);
console.log(nodes);


  useEffect(() => {
    fetch('/graph_layout_star.csv')
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
  const layer = new ScatterplotLayer({
    id: 'scatterplot-layer',
    // data works --> why not the file data?
    nodes,
    getPosition: d => [d.Long1, d.Lat1],
    getFillColor: [255, 0,0],
    getRadius: 100000,
  });
  console.log(layer);
  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      layers= {[layer]}
    />
  );
}
