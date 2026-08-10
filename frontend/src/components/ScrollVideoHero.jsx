import React, { useRef, useEffect, useState } from 'react';
import { Sparkles, ArrowDown, Cpu, Zap, Headphones, Smartphone, Laptop, ShieldCheck, Award, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLenis } from '../context/LenisContext';

const storeQualities = [
  { icon: ShieldCheck, title: '2-Year Quantum Warranty', desc: 'Full international hardware coverage', color: 'text-blue-400' },
  { icon: Zap, title: 'Same-Day Express Dispatch', desc: 'Automated glass hub order fulfillment', color: 'text-cyan-400' },
  { icon: Award, title: '100% Genuine Titanium', desc: 'Verified original component manufacturing', color: 'text-indigo-400' },
  { icon: Headphones, title: 'Acoustic Glass Chamber', desc: 'Zero-resonance spatial audio engineering', color: 'text-blue-400' },
  { icon: Cpu, title: 'Quantum M4 Silicon', desc: 'Next-gen neural architecture processing', color: 'text-cyan-400' },
  { icon: Sparkles, title: '24/7 Priority Support', desc: 'Dedicated concierge technical team', color: 'text-indigo-400' },
  { icon: ShieldCheck, title: '30-Day Risk-Free Returns', desc: '100% full money-back guarantee policy', color: 'text-blue-400' },
];

/**
 * ScrollVideoHero Component:
 * Interactive hero section combining Lenis scroll scrubbing, HTML5 video canvas frame-playback,
 * glassmorphism overlay badges, and dynamic product feature cards.
 */
const ScrollVideoHero = ({ onExploreClick }) => {
  const containerRef = useRef(null);
  const video1Ref = useRef(null);
  const video2Ref = useRef(null);
  const video3Ref = useRef(null);

  const lenis = useLenis();

  const [v1Loaded, setV1Loaded] = useState(false);
  const [v2Loaded, setV2Loaded] = useState(false);
  const [v3Loaded, setV3Loaded] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [activeSegment, setActiveSegment] = useState(1);

  // Handle Video Preloading (Buffers until readyState >= 4 HAVE_ENOUGH_DATA / canplaythrough)
  useEffect(() => {
    const v1 = video1Ref.current;
    const v2 = video2Ref.current;
    const v3 = video3Ref.current;

    const handleV1Ready = () => {
      setV1Loaded(true);
      if (v1 && v1.currentTime === 0) v1.currentTime = 0.01;
    };

    const handleV2Ready = () => {
      setV2Loaded(true);
      if (v2 && v2.currentTime === 0) v2.currentTime = 0.01;
    };

    const handleV3Ready = () => {
      setV3Loaded(true);
      if (v3 && v3.currentTime === 0) v3.currentTime = 0.01;
    };

    const handleV1Error = (e) => {
      console.warn('Video 1 load fallback:', e);
      setV1Loaded(true);
    };

    const handleV2Error = (e) => {
      console.warn('Video 2 load fallback:', e);
      setV2Loaded(true);
    };

    const handleV3Error = (e) => {
      console.warn('Video 3 load fallback:', e);
      setV3Loaded(true);
    };

    const safetyTimeout = setTimeout(() => {
      setV1Loaded(true);
      setV2Loaded(true);
      setV3Loaded(true);
    }, 4500);

    if (v1) {
      if (v1.readyState >= 4) {
        handleV1Ready();
      } else {
        v1.addEventListener('canplaythrough', handleV1Ready);
        v1.addEventListener('canplay', handleV1Ready);
        v1.addEventListener('error', handleV1Error);
      }
    }

    if (v2) {
      if (v2.readyState >= 4) {
        handleV2Ready();
      } else {
        v2.addEventListener('canplaythrough', handleV2Ready);
        v2.addEventListener('canplay', handleV2Ready);
        v2.addEventListener('error', handleV2Error);
      }
    }

    if (v3) {
      if (v3.readyState >= 4) {
        handleV3Ready();
      } else {
        v3.addEventListener('canplaythrough', handleV3Ready);
        v3.addEventListener('canplay', handleV3Ready);
        v3.addEventListener('error', handleV3Error);
      }
    }

    return () => {
      clearTimeout(safetyTimeout);
      if (v1) {
        v1.removeEventListener('canplaythrough', handleV1Ready);
        v1.removeEventListener('canplay', handleV1Ready);
        v1.removeEventListener('error', handleV1Error);
      }
      if (v2) {
        v2.removeEventListener('canplaythrough', handleV2Ready);
        v2.removeEventListener('canplay', handleV2Ready);
        v2.removeEventListener('error', handleV2Error);
      }
      if (v3) {
        v3.removeEventListener('canplaythrough', handleV3Ready);
        v3.removeEventListener('canplay', handleV3Ready);
        v3.removeEventListener('error', handleV3Error);
      }
    };
  }, []);

  const isFullyLoaded = v1Loaded && v2Loaded && v3Loaded;

  // Drive video scrub from Lenis scroll event
  useEffect(() => {
    if (!lenis) return;

    let rafId = null;

    const updateVideoFrame = () => {
      const container = containerRef.current;
      const v1 = video1Ref.current;
      const v2 = video2Ref.current;
      const v3 = video3Ref.current;

      if (container && v1 && v2 && v3) {
        const rect = container.getBoundingClientRect();
        const totalScrollable = rect.height - window.innerHeight;

        if (totalScrollable > 0) {
          const currentScroll = -rect.top;
          const rawProgress = Math.max(0, Math.min(1, currentScroll / totalScrollable));

          setScrollProgress(rawProgress);

          const oneThird = 1 / 3;
          const twoThirds = 2 / 3;

          if (rawProgress < oneThird) {
            // Segment 1: iPhone 17 Pro Max (0% - 33.3%)
            setActiveSegment(1);
            const subProgress = rawProgress / oneThird;
            if (isFinite(v1.duration) && v1.duration > 0) {
              v1.currentTime = Math.min(v1.duration - 0.01, Math.max(0.01, subProgress * v1.duration));
            }
          } else if (rawProgress < twoThirds) {
            // Segment 2: AirPods & Glass Case (33.3% - 66.6%)
            setActiveSegment(2);
            const subProgress = (rawProgress - oneThird) / oneThird;
            if (isFinite(v2.duration) && v2.duration > 0) {
              v2.currentTime = Math.min(v2.duration - 0.01, Math.max(0.01, subProgress * v2.duration));
            }
          } else {
            // Segment 3: Quantum MacBook Pro (66.6% - 100%)
            setActiveSegment(3);
            const subProgress = (rawProgress - twoThirds) / oneThird;
            if (isFinite(v3.duration) && v3.duration > 0) {
              v3.currentTime = Math.min(v3.duration - 0.01, Math.max(0.01, subProgress * v3.duration));
            }
          }
        }
      }
    };

    const handleLenisScroll = () => {
      if (rafId) {
        cancelAnimationFrame(rafId);
      }

      rafId = requestAnimationFrame(updateVideoFrame);
    };

    updateVideoFrame();
    lenis.on('scroll', handleLenisScroll);

    return () => {
      lenis.off('scroll', handleLenisScroll);
      if (rafId) {
        cancelAnimationFrame(rafId);
      }
    };
  }, [lenis]);

  return (
    <div ref={containerRef} className="relative h-[750vh] bg-black">
      {/* Sticky Viewport Container */}
      <div className="sticky top-0 h-screen w-full flex flex-col justify-between overflow-hidden bg-[#07070b] pt-16">
        
        {/* Ambient Radial Glow */}
        <div className="absolute inset-0 bg-gradient-radial from-blue-600/15 via-transparent to-transparent pointer-events-none" />

        {/* Preload Loading Spinner */}
        {!isFullyLoaded && (
          <div className="absolute inset-0 z-40 flex flex-col items-center justify-center space-y-3 p-6 glass-panel rounded-2xl border border-white/10 m-auto w-fit h-fit">
            <div className="w-8 h-8 border-3 border-blue-400 border-t-transparent rounded-full animate-spin" />
            <span className="text-xs font-semibold text-slate-300">
              Preloading 3-Phase Quantum Hardware Stream...
            </span>
          </div>
        )}

        {/* Video Canvas Container (Clean, unobstructed video window) */}
        <div className="relative w-full max-w-[1280px] h-[calc(100vh-140px)] mx-auto overflow-hidden rounded-3xl border border-white/10 shadow-[0_0_80px_rgba(77,166,255,0.25)] bg-black my-auto">
          
          {/* Video 1: iPhone 17 Pro Max */}
          <video
            ref={video1Ref}
            src="/videos/iPhone_17_Pro_Max_materializes_scrub-ready.mp4"
            muted
            playsInline
            preload="auto"
            style={{ opacity: activeSegment === 1 ? 1 : 0 }}
            className="absolute inset-0 w-full h-full object-cover object-center transition-opacity duration-300 filter brightness-95 contrast-105"
          />

          {/* Video 2: AirPods & Glass Case */}
          <video
            ref={video2Ref}
            src="/videos/Earbuds_and_case_materialize_scrub-ready.mp4"
            muted
            playsInline
            preload="auto"
            style={{ opacity: activeSegment === 2 ? 1 : 0 }}
            className="absolute inset-0 w-full h-full object-cover object-center transition-opacity duration-300 filter brightness-95 contrast-105"
          />

          {/* Video 3: Quantum MacBook Pro */}
          <video
            ref={video3Ref}
            src="/videos/Laptop_materializing_scrub-ready.mp4"
            muted
            playsInline
            preload="auto"
            style={{ opacity: activeSegment === 3 ? 1 : 0 }}
            className="absolute inset-0 w-full h-full object-cover object-center transition-opacity duration-300 filter brightness-95 contrast-105"
          />

          {/* Vignette Overlays */}
          <div className="absolute inset-0 bg-gradient-to-t from-[#07070b] via-transparent to-[#07070b]/60 pointer-events-none" />
          <div className="absolute inset-0 bg-gradient-to-r from-[#07070b]/70 via-transparent to-[#07070b]/70 pointer-events-none" />

          {/* Clean Floating UI Overlays */}
          <div className="absolute inset-0 z-20 flex flex-col justify-between p-6 md:p-10 pointer-events-none">
            
            {/* Top Bar: Sequence Indicator & Specs Badge */}
            <div className="flex items-center justify-between">
              {/* Product Pill Label */}
              <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full glass-pill border-blue-500/40 text-blue-300 text-xs font-bold tracking-wider shadow-lg">
                <Sparkles className="w-3.5 h-3.5 animate-spin text-blue-400" />
                <span>
                  {activeSegment === 1 && 'PRODUCT 01 / 03 • IPHONE 17 PRO MAX'}
                  {activeSegment === 2 && 'PRODUCT 02 / 03 • AIRPODS & GLASS CASE'}
                  {activeSegment === 3 && 'PRODUCT 03 / 03 • QUANTUM MACBOOK PRO'}
                </span>
              </div>

              {/* Dynamic Spec Badges */}
              <div className="hidden sm:flex items-center space-x-4 text-xs font-semibold text-slate-300">
                {activeSegment === 1 && (
                  <>
                    <span className="flex items-center space-x-1"><Smartphone className="w-3.5 h-3.5 text-blue-400" /><span>200MP Periscope</span></span>
                    <span className="flex items-center space-x-1"><Cpu className="w-3.5 h-3.5 text-cyan-400" /><span>A19 Quantum Bionic</span></span>
                  </>
                )}
                {activeSegment === 2 && (
                  <>
                    <span className="flex items-center space-x-1"><Headphones className="w-3.5 h-3.5 text-blue-400" /><span>Hybrid ANC -45dB</span></span>
                    <span className="flex items-center space-x-1"><Zap className="w-3.5 h-3.5 text-indigo-400" /><span>45h Spatial Audio</span></span>
                  </>
                )}
                {activeSegment === 3 && (
                  <>
                    <span className="flex items-center space-x-1"><Laptop className="w-3.5 h-3.5 text-blue-400" /><span>M4 Quantum Max</span></span>
                    <span className="flex items-center space-x-1"><Sparkles className="w-3.5 h-3.5 text-cyan-400" /><span>Liquid Retina XDR 120Hz</span></span>
                  </>
                )}
              </div>
            </div>

            {/* Middle Clean Title */}
            <div className="max-w-2xl mx-auto text-center space-y-3 my-auto">
              <AnimatePresence mode="wait">
                {activeSegment === 1 && (
                  <motion.div
                    key="seg1"
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -15 }}
                    transition={{ duration: 0.3 }}
                    className="space-y-2"
                  >
                    <div className="inline-block px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-[11px] font-mono font-bold border border-blue-400/30">
                      PHASE 1: HARDWARE MATERIALIZATION
                    </div>
                    <h1 className="text-4xl md:text-6xl font-black text-white tracking-tight leading-none drop-shadow-2xl">
                      iPhone 17 Pro Max <br />
                      <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 text-glow">
                        Pure Titanium Glass
                      </span>
                    </h1>
                  </motion.div>
                )}

                {activeSegment === 2 && (
                  <motion.div
                    key="seg2"
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -15 }}
                    transition={{ duration: 0.3 }}
                    className="space-y-2"
                  >
                    <div className="inline-block px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-[11px] font-mono font-bold border border-cyan-400/30">
                      PHASE 2: ACOUSTIC GLASS MATERIALIZATION
                    </div>
                    <h2 className="text-4xl md:text-6xl font-black text-white tracking-tight leading-none drop-shadow-2xl">
                      Nexus AirPods <br />
                      <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-400 to-indigo-400 text-glow">
                        Transparent Sound Case
                      </span>
                    </h2>
                  </motion.div>
                )}

                {activeSegment === 3 && (
                  <motion.div
                    key="seg3"
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -15 }}
                    transition={{ duration: 0.3 }}
                    className="space-y-2"
                  >
                    <div className="inline-block px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-[11px] font-mono font-bold border border-indigo-400/30">
                      PHASE 3: QUANTUM COMPUTING MATERIALIZATION
                    </div>
                    <h2 className="text-4xl md:text-6xl font-black text-white tracking-tight leading-none drop-shadow-2xl">
                      MacBook Pro <br />
                      <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-300 via-blue-400 to-cyan-300 text-glow">
                        Quantum M4 Silicon
                      </span>
                    </h2>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* End of Hero CTA */}
              {scrollProgress >= 0.85 && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="pt-2 pointer-events-auto"
                >
                  <button
                    onClick={onExploreClick}
                    className="btn-glow px-8 py-3.5 rounded-full font-bold text-xs text-white cursor-pointer shadow-2xl"
                  >
                    Explore Full Store Catalog
                  </button>
                </motion.div>
              )}
            </div>

            {/* Bottom Scroll Prompt Indicator */}
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span className="text-[11px] font-semibold text-slate-400 hidden sm:inline">
                NEXUS QUANTUM ELECTRONICS
              </span>
              <div className="flex items-center space-x-1 animate-bounce text-slate-300">
                <span className="text-[11px] font-bold">
                  {scrollProgress < (1 / 3) && 'SCROLL TO MATERIALIZE AIRPODS'}
                  {scrollProgress >= (1 / 3) && scrollProgress < (2 / 3) && 'SCROLL TO MATERIALIZE MACBOOK'}
                  {scrollProgress >= (2 / 3) && 'SCROLL TO EXPLORE STORE'}
                </span>
                <ArrowDown className="w-3.5 h-3.5 text-blue-400" />
              </div>
            </div>

          </div>

        </div>

        {/* Bottom Horizontal Moving Cards Track (Scroll-Driven Right to Left Ticker) */}
        <div className="w-full bg-[#07070b]/90 border-t border-white/10 py-3 overflow-hidden relative z-30 shadow-2xl shrink-0">
          <div className="flex items-center space-x-6 overflow-hidden">
            <motion.div
              style={{ x: `calc(-${scrollProgress * 50}% + 0px)` }}
              className="flex space-x-4 shrink-0 transition-transform duration-75 ease-out px-4"
            >
              {[...storeQualities, ...storeQualities].map((item, idx) => {
                const IconComp = item.icon;
                return (
                  <div
                    key={idx}
                    className="glass-panel px-5 py-2.5 rounded-2xl flex items-center space-x-3 border border-white/10 shrink-0 min-w-[260px] shadow-lg hover:border-blue-400/40 transition-colors"
                  >
                    <div className="w-8 h-8 rounded-xl bg-blue-500/10 border border-blue-400/20 flex items-center justify-center text-blue-400 shrink-0">
                      <IconComp className="w-4 h-4" />
                    </div>
                    <div className="min-w-0">
                      <h4 className="text-xs font-bold text-white truncate">{item.title}</h4>
                      <p className="text-[10px] text-slate-400 truncate">{item.desc}</p>
                    </div>
                  </div>
                );
              })}
            </motion.div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ScrollVideoHero;
