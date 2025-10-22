import React, { useEffect, useMemo, useRef, useState } from 'react'
import {
  Background,
  Controls,
  MiniMap,
  Node,
  ReactFlow,
  ReactFlowProvider,
  useReactFlow
} from '@xyflow/react'
import '@xyflow/react/dist/base.css'
import type { Slide } from './types'

function useQueryId() {
  const [id, setId] = useState<string | null>(null)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    setId(params.get('id'))
  }, [])

  return id
}

function useViewportController() {
  const api = useReactFlow()

  const animateTo = (slide: Slide) => {
    api.setViewport(
      {
        x: -slide.x + 240,
        y: -slide.y + 160,
        zoom: slide.zoom ?? 1
      },
      { duration: 650 }
    )
  }

  return { animateTo }
}

function PreziCanvas() {
  const [slides, setSlides] = useState<Slide[]>([])
  const [current, setCurrent] = useState(0)
  const queryId = useQueryId()
  const { animateTo } = useViewportController()
  const idxRef = useRef(0)

  useEffect(() => {
    const url = `${import.meta.env.BASE_URL}slides.json`
    fetch(url, { cache: 'no-store' })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load slides.json: ${response.status}`)
        }
        return response.json()
      })
      .then((data: Slide[]) => setSlides(data))
      .catch(error => console.error(error))
  }, [])

  const activeId = slides[current]?.id

  const nodes: Node[] = useMemo(
    () =>
      slides.map((slide) => ({
        id: slide.id,
        position: { x: slide.x, y: slide.y },
        data: {
          label: (
            <div style={{ maxWidth: 360 }}>
              <div style={{ fontWeight: 600, marginBottom: 6 }}>{slide.title}</div>
              <div>
                <a href={slide.mdPath}>Read</a>
              </div>
            </div>
          )
        },
        style: {
          padding: 12,
          borderRadius: 10,
          border: slide.id === activeId ? '2px solid #0b5fff' : '1px solid #d0d0d0',
          background: 'white',
          boxShadow: slide.id === activeId ? '0 6px 12px rgba(11, 95, 255, 0.2)' : '0 4px 10px rgba(15, 23, 42, 0.08)'
        }
      })),
    [slides, activeId]
  )

  useEffect(() => {
    if (!slides.length) {
      return
    }

    let startIndex = 0
    if (queryId) {
      const foundIndex = slides.findIndex(slide => slide.id === queryId)
      if (foundIndex >= 0) {
        startIndex = foundIndex
      }
    }

    idxRef.current = startIndex
    setCurrent(startIndex)
    animateTo(slides[startIndex])
  }, [slides, queryId, animateTo])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (!slides.length) {
        return
      }

      if (event.key === 'ArrowRight') {
        idxRef.current = Math.min(idxRef.current + 1, slides.length - 1)
        setCurrent(idxRef.current)
        animateTo(slides[idxRef.current])
      } else if (event.key === 'ArrowLeft') {
        idxRef.current = Math.max(idxRef.current - 1, 0)
        setCurrent(idxRef.current)
        animateTo(slides[idxRef.current])
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [slides, animateTo])

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow nodes={nodes} edges={[]} panOnDrag zoomOnScroll fitView>
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  )
}

export default function App() {
  return (
    <ReactFlowProvider>
      <PreziCanvas />
    </ReactFlowProvider>
  )
}
