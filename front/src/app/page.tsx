"use client";

import { useState, useEffect } from "react";
import { 
  Activity, AlertTriangle, BarChart3, Building, Map, Coins, Radar, 
  Search, RefreshCw, Download, FileText, ArrowRight, Home as HomeIcon, CheckCircle2, Info 
} from "lucide-react";

export default function Home() {
  // Inputs manuales
  const [municipio, setMunicipio] = useState("Bilbao");
  const [precio, setPrecio] = useState(120);
  const [disponibilidad, setDisponibilidad] = useState(280);
  const [description, setDescription] = useState("");
  const [hostAbout, setHostAbout] = useState("");

  // Inputs de URL
  const [urlInput, setUrlInput] = useState("");
  const [analyzedListing, setAnalyzedListing] = useState<any>(null);

  // Estado general de datos
  const [data, setData] = useState({
    ratio_especulacion: 0.0,
    indice_desplazamiento: 0.0,
    probabilidad_m1: 0.0,
    probabilidad_m2: 0.0,
    impacto_economico: 0.0,
    ratio_explotacion_comercial: 0.0,
    eustat_poblacion_joven: 0.0,
    eustat_desertizacion_comercio: 0.0,
    detalles: {
      renta_media_m2: 0.0,
      alquiler_residencial_estimado: 0.0,
      host_listings_count: 1,
      dias_ocupados_proyectados: 0,
      ingreso_mensual_vut_estimado: 0.0
    }
  });

  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"manual" | "url">("manual");
  const [errorMsg, setErrorMsg] = useState("");

  const [loadingTextIndex, setLoadingTextIndex] = useState(0);
  const loadingTexts = [
    "> Extrayendo datos de URL...",
    "> Burlando sistemas anti-bots...",
    "> Inyectando Meta-Features en Módulo 3...",
    "> Calculando impacto territorial..."
  ];

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (loading) {
      setLoadingTextIndex(0);
      interval = setInterval(() => {
        setLoadingTextIndex((prev) => (prev + 1) % loadingTexts.length);
      }, 1200);
    }
    return () => clearInterval(interval);
  }, [loading]);

  // Carga reactiva para cambios manuales
  useEffect(() => {
    if (activeTab === "manual") {
      const fetchManualData = async () => {
        setLoading(true);
        try {
          const response = await fetch("http://127.0.0.1:8000/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              municipio,
              precio_por_noche: precio,
              disponibilidad,
              description,
              host_about: hostAbout
            })
          });
          if (response.ok) {
            const result = await response.json();
            setData(result);
          }
        } catch (error) {
          console.error("Error connecting to API:", error);
        }
        setLoading(false);
      };

      const delayDebounce = setTimeout(() => {
        fetchManualData();
      }, 250);

      return () => clearTimeout(delayDebounce);
    }
  }, [municipio, precio, disponibilidad, description, hostAbout, activeTab]);

  // Manejador para auditar URL de Airbnb/Booking
  const handleUrlAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!urlInput.trim()) return;
    
    setLoading(true);
    setErrorMsg("");
    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: urlInput })
      });
      
      if (response.ok) {
        const result = await response.json();
        setAnalyzedListing(result);
        setData(result.analysis);
        setActiveTab("url");
      } else {
        setErrorMsg("No se pudo auditar la URL. Comprueba el formato e inténtalo de nuevo.");
      }
    } catch (error) {
      setErrorMsg("Error de conexión con el backend de auditoría.");
      console.error(error);
    }
    setLoading(false);
  };

  // Resetear y volver a modo manual
  const handleReset = () => {
    setAnalyzedListing(null);
    setActiveTab("manual");
    setUrlInput("");
    // Forzar actualización inmediata
    setPrecio(120);
    setDisponibilidad(280);
    setMunicipio("Bilbao");
    setDescription("");
    setHostAbout("");
  };

  // Descarga del diagnóstico forense en JSON
  const downloadForenseReport = () => {
    const reportData = {
      timestamp: new Date().toISOString(),
      fuente: "Especulómetro Vasco v1.5",
      analisis_tipo: activeTab === "url" ? "URL Guerrilla" : "Simulación Manual",
      alojamiento: activeTab === "url" ? {
        titulo: analyzedListing?.title,
        url: urlInput,
        host: analyzedListing?.host_name,
        host_alojamientos_totales: analyzedListing?.host_listings_count,
        municipio: analyzedListing?.municipio,
        precio_noche: analyzedListing?.price,
        disponibilidad_anual: analyzedListing?.availability
      } : {
        municipio,
        precio_noche_control: precio,
        disponibilidad_anual_control: disponibilidad
      },
      indicadores_ia: {
        especulometro_m1_prob_gran_tenedor: `${data.ratio_especulacion}%`,
        cazapiratas_m2_prob_irregularidad: `${data.indice_desplazamiento}%`,
        oraculo_urbano_m3_presion_alquiler: `+${data.impacto_economico} €/m²`,
        alerta_tenencia_profesional: data.ratio_especulacion > 60 ? "CRÍTICA" : "NORMAL"
      },
      impacto_social: {
        ratio_rentabilidad_vut_vs_residencial: `${data.ratio_explotacion_comercial}x`,
        eustat_tasa_fuga_jovenes: `-${data.eustat_poblacion_joven}% (5 años)`,
        eustat_desertizacion_comercial: `${data.eustat_desertizacion_comercio}%`
      }
    };

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(reportData, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `informe_forense_${data.detalles.municipio_procesado || municipio}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  // Cálculos dinámicos para el Donut Chart SVG
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (data.ratio_especulacion / 100) * circumference;

  const m1Ratio = data.ratio_especulacion;
  const isM1Red = m1Ratio > 66;
  const isM1Yellow = m1Ratio > 33 && m1Ratio <= 66;
  const isM1Green = m1Ratio <= 33;
  
  const m1StrokeClass = isM1Red ? 'stroke-red-500' : isM1Yellow ? 'stroke-yellow-400' : 'stroke-emerald-400';
  const m1GlowClass = isM1Red ? 'neon-glow-red text-red-500' : isM1Yellow ? 'drop-shadow-[0_0_8px_rgba(250,204,21,0.8)] text-yellow-400' : 'neon-glow-emerald text-emerald-400';
  const m1BorderClass = isM1Red ? 'border-red-500/30 bg-red-500/5' : isM1Yellow ? 'border-yellow-400/20 bg-yellow-400/5' : 'border-emerald-400/20 bg-emerald-400/5';

  const m2Ratio = data.indice_desplazamiento;
  const isM2High = m2Ratio > 60;
  const isM2Low = m2Ratio < 40;
  
  const m2BorderClass = isM2High 
    ? 'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.3)] bg-red-500/5' 
    : isM2Low 
      ? 'border-emerald-500/50 text-emerald-400 bg-emerald-500/5' 
      : 'border-orange-500/50 bg-orange-500/5 text-orange-400';
  
  const m2StrokeClass = isM2High ? 'stroke-red-500' : isM2Low ? 'stroke-emerald-500' : 'stroke-orange-500';
  const m2TextClass = isM2High ? 'text-red-500' : isM2Low ? 'text-emerald-400' : 'text-orange-400';
  const m2StrokeDashoffset = circumference - (m2Ratio / 100) * circumference;

  return (
    <div className="min-h-screen text-gray-100 flex flex-col justify-between">
      
      {/* Cabecera Principal */}
      <header className="border-b border-white/5 py-4 px-6 md:px-12 flex justify-between items-center bg-[#0F1115]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="bg-cyan-500/10 p-2 rounded-xl border border-cyan-500/20">
            <Radar className="text-cyan-400 w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-wider text-white flex items-center gap-2">
              ESPECULÓMETRO
            </h1>
          </div>
        </div>
        <div className="text-xs text-gray-500 font-mono hidden md:block">
          import antigravity 🚀 <span className="text-gray-700">|</span> Haciendo volar el software libre sobre el suelo vasco.
        </div>
      </header>

      {/* Main Container */}
      <div className="flex-1 flex flex-col lg:flex-row max-w-7xl w-full mx-auto p-4 md:p-8 gap-8">
        
        {/* MÓDULO IZQUIERDO: Panel de Control (Sidebar) */}
        <aside className="rounded-2xl p-6 w-full lg:w-80 flex-shrink-0 flex flex-col gap-6 self-start lg:sticky lg:top-24 bg-[#12151A]/90 border border-white/10 shadow-2xl shadow-black/80 backdrop-blur-xl z-40">
          
          <div className="border-b border-white/5 pb-4">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest">Auditoría</h2>
            <p className="text-xs text-gray-500 mt-1">Configura las variables manuales o analiza un enlace web.</p>
          </div>

          {/* URL Guerrilla Input Form */}
          <form onSubmit={handleUrlAudit} className="space-y-3">
            <label className="text-xs font-semibold text-gray-400 flex items-center gap-2">
              <Search className="w-3.5 h-3.5 text-cyan-400" /> AUDITAR URL DE GUERRILLA
            </label>
            <div className="flex gap-2">
              <input 
                type="text" 
                placeholder="Pegar URL de Airbnb o Booking..."
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                className="flex-1 bg-black/40 border border-white/5 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500/50 transition-colors placeholder:text-gray-600"
              />
              <button 
                type="submit" 
                disabled={loading}
                className="bg-cyan-500 hover:bg-cyan-600 text-black font-semibold rounded-lg px-3 py-2 text-xs transition-colors flex items-center justify-center disabled:opacity-50"
              >
                {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : "Auditar"}
              </button>
            </div>
            {errorMsg && <p className="text-[10px] text-red-400">{errorMsg}</p>}
            {loading && activeTab === "url" && (
              <div className="mt-2 p-3 bg-black/60 rounded-lg border border-cyan-500/30 text-cyan-400 font-mono text-xs animate-pulse">
                {loadingTexts[loadingTextIndex]}
              </div>
            )}
          </form>

          <div className="relative flex py-2 items-center">
            <div className="flex-grow border-t border-white/5"></div>
            <span className="flex-shrink mx-3 text-[10px] text-gray-600 uppercase tracking-widest font-mono">o control manual</span>
            <div className="flex-grow border-t border-white/5"></div>
          </div>

          {/* Manual sliders and selectors */}
          <div className={`space-y-6 ${activeTab === "url" ? "opacity-30 pointer-events-none" : ""}`}>
            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-400 flex items-center gap-2">
                <Map className="w-3.5 h-3.5 text-cyan-400" /> Capital a Auditar
              </label>
              <select 
                value={municipio}
                onChange={(e) => setMunicipio(e.target.value)}
                className="w-full bg-black/40 border border-white/5 rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-500/50 transition-colors"
              >
                <option value="Bilbao">Bilbao</option>
                <option value="San Sebastián">Donostia-San Sebastián</option>
                <option value="Vitoria-Gasteiz">Vitoria-Gasteiz</option>
              </select>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-gray-400 flex items-center gap-2">
                  <Coins className="w-3.5 h-3.5 text-orange-neon" /> Tarifa por Noche
                </span>
                <span className="text-white font-mono">{precio} €</span>
              </div>
              <input 
                type="range" 
                min="30" 
                max="500" 
                value={precio}
                onChange={(e) => setPrecio(Number(e.target.value))}
                className="w-full accent-orange-500 h-1.5 bg-black/40 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-[9px] text-gray-600 font-mono">
                <span>30€</span>
                <span>500€</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-gray-400 flex items-center gap-2">
                  <Building className="w-3.5 h-3.5 text-cyan-400" /> Disponibilidad Anual
                </span>
                <span className="text-white font-mono">{disponibilidad} días</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="365" 
                value={disponibilidad}
                onChange={(e) => setDisponibilidad(Number(e.target.value))}
                className="w-full accent-cyan-500 h-1.5 bg-black/40 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-[9px] text-gray-600 font-mono">
                <span>0 días (Ocupado)</span>
                <span>365 días (Cartel)</span>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-400 flex items-center gap-2">
                <FileText className="w-3.5 h-3.5 text-cyan-400" /> Descripción del Anuncio (NLP)
              </label>
              <textarea 
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Ej: Luxury flat managed by agency..."
                className="w-full bg-black/40 border border-white/5 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500/50 transition-colors h-20 resize-none placeholder:text-gray-600"
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-400 flex items-center gap-2">
                <FileText className="w-3.5 h-3.5 text-cyan-400" /> Perfil del Anfitrión (NLP)
              </label>
              <textarea 
                value={hostAbout}
                onChange={(e) => setHostAbout(e.target.value)}
                placeholder="Ej: We are an elite property team..."
                className="w-full bg-black/40 border border-white/5 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500/50 transition-colors h-16 resize-none placeholder:text-gray-600"
              />
            </div>
          </div>

          {activeTab === "url" && (
            <button 
              onClick={handleReset}
              className="mt-2 w-full bg-white/5 hover:bg-white/10 text-white border border-white/10 rounded-lg py-2.5 text-xs font-semibold transition-all flex items-center justify-center gap-2"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Volver a Control Manual
            </button>
          )}

        </aside>

        {/* CONTENEDOR CENTRAL: Módulos Superiores e Inferiores */}
        <main className="flex-1 flex flex-col gap-6">
          
          {/* Ficha del Alojamiento Scrapeado (si aplica) */}
          {activeTab === "url" && analyzedListing && (
            <div className="glass-panel rounded-2xl p-4 flex flex-col sm:flex-row gap-4 border-cyan-500/20 relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-cyan-500/10 text-cyan-400 border-l border-b border-cyan-500/20 px-3 py-1 text-[10px] font-mono rounded-bl-lg uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="w-3 h-3 text-cyan-400" /> Alojamiento Auditado de Guerrilla
              </div>
              <img 
                src={analyzedListing.image} 
                alt="Airbnb" 
                className="w-full sm:w-32 h-24 object-cover rounded-xl border border-white/5 flex-shrink-0"
              />
              <div className="flex-1 flex flex-col justify-between py-1">
                <div>
                  <h3 className="text-base font-bold text-white leading-tight mb-1">{analyzedListing.title}</h3>
                  <p className="text-xs text-gray-400 flex items-center gap-1.5">
                    <Map className="w-3 h-3 text-cyan-400" /> {analyzedListing.municipio}
                  </p>
                </div>
                <div className="flex flex-wrap gap-4 text-xs font-mono mt-3 sm:mt-0">
                  <span className="text-gray-400">Anfitrión: <strong className="text-white">{analyzedListing.host_name}</strong></span>
                  <span className="text-gray-700">|</span>
                  <span className="text-gray-400">Cartera: <strong className="text-cyan-400">{analyzedListing.host_listings_count} anuncios</strong></span>
                  <span className="text-gray-700">|</span>
                  <span className="text-gray-400">Tarifa: <strong className="text-white">{analyzedListing.price}€/noche</strong></span>
                  <span className="text-gray-700">|</span>
                  <span className="text-gray-400">Oferta: <strong className="text-white">{analyzedListing.availability}d/año</strong></span>
                </div>
              </div>
            </div>
          )}

          {/* MÓDULO CENTRAL SUPERIOR: El Panel Tri-Modular (Métricas de la IA) */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Tarjeta 1: El Especulómetro */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col items-center justify-between min-h-[220px] shadow-lg shadow-black/50 transition-all relative group ${!loading ? m1BorderClass : ''}`}>
              <div className="w-full flex items-center justify-between text-xs font-semibold relative z-10">
                <span className="text-gray-400 uppercase tracking-wider flex items-center gap-2">
                  <AlertTriangle className={`w-4 h-4 ${!loading ? (isM1Red ? 'text-red-500' : isM1Yellow ? 'text-yellow-400' : 'text-emerald-400') : 'text-gray-500'}`} /> Especulómetro
                  <div className="relative group/tooltip">
                    <Info className="w-3.5 h-3.5 text-gray-500 hover:text-white cursor-pointer" />
                    <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-48 p-2 bg-black/95 border border-white/10 text-[10px] text-gray-300 rounded shadow-xl opacity-0 group-hover/tooltip:opacity-100 transition-opacity pointer-events-none z-50 normal-case tracking-normal">
                      Identifica si el propietario opera múltiples pisos (gran tenedor) actuando como una empresa bajo el radar.
                    </div>
                  </div>
                </span>
                <span className="text-[10px] text-gray-500 font-mono">MÓDULO M1</span>
              </div>
              
              {loading ? (
                <div className="flex flex-col items-center justify-center my-3 w-full space-y-4">
                  <div className="w-24 h-24 rounded-full bg-gray-800 animate-pulse border-[8px] border-gray-700/50"></div>
                  <div className="w-3/4 h-6 bg-gray-800 animate-pulse rounded"></div>
                </div>
              ) : (
                <>
                  {/* Donut Chart SVG */}
                  <div className="relative w-28 h-28 flex items-center justify-center my-3">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle 
                        cx="50" cy="50" r={radius} 
                        className="stroke-black/30 fill-none" 
                        strokeWidth="8"
                      />
                      <circle 
                        cx="50" cy="50" r={radius} 
                        className={`fill-none transition-all duration-700 ease-out ${m1StrokeClass}`} 
                        strokeWidth="8"
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center justify-center">
                      <span className={`text-2xl font-bold font-mono ${m1GlowClass}`}>
                        {data.ratio_especulacion.toFixed(0)}%
                      </span>
                      <span className="text-[8px] text-gray-500 uppercase tracking-widest">Multi-Host</span>
                    </div>
                  </div>

                  <div className="w-full text-center">
                    {isM1Red ? (
                      <span className="text-[10px] font-bold text-red-500 bg-red-500/10 px-2.5 py-1 rounded border border-red-500/20 block animate-pulse">
                        Alerta: Explotación Profesional/Multi-host
                      </span>
                    ) : isM1Yellow ? (
                      <span className="text-[10px] font-bold text-yellow-400 bg-yellow-400/10 px-2.5 py-1 rounded border border-yellow-400/20 block">
                        Aviso: Actividad Comercial Moderada
                      </span>
                    ) : (
                      <span className="text-[10px] text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20 block">
                        Particular / Operación moderada
                      </span>
                    )}
                  </div>
                </>
              )}
            </div>

            {/* Tarjeta 2: El Cazapiratas */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col justify-between min-h-[220px] shadow-lg shadow-black/50 transition-all relative group ${!loading ? m2BorderClass : ''}`}>
              <div className="w-full flex items-center justify-between text-xs font-semibold relative z-10">
                <span className="text-gray-400 uppercase tracking-wider flex items-center gap-2">
                  <Building className={`w-4 h-4 ${!loading ? m2TextClass : 'text-gray-500'}`} /> El Cazapiratas
                  <div className="relative group/tooltip">
                    <Info className="w-3.5 h-3.5 text-gray-500 hover:text-white cursor-pointer" />
                    <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-48 p-2 bg-black/95 border border-white/10 text-[10px] text-gray-300 rounded shadow-xl opacity-0 group-hover/tooltip:opacity-100 transition-opacity pointer-events-none z-50 normal-case tracking-normal">
                      Calcula la probabilidad de que la licencia turística no exista o sea fraudulenta en base a cruce de datos.
                    </div>
                  </div>
                </span>
                <span className="text-[10px] text-gray-500 font-mono">MÓDULO M2</span>
              </div>

              {loading ? (
                <div className="flex flex-col items-center justify-center my-3 w-full space-y-4">
                  <div className="w-24 h-24 rounded-full bg-gray-800 animate-pulse border-[8px] border-gray-700/50"></div>
                  <div className="w-3/4 h-6 bg-gray-800 animate-pulse rounded"></div>
                </div>
              ) : (
                <>
                  {/* Donut Chart SVG M2 */}
                  <div className="relative w-28 h-28 flex items-center justify-center my-3 mx-auto">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle 
                        cx="50" cy="50" r={radius} 
                        className="stroke-black/30 fill-none" 
                        strokeWidth="8"
                      />
                      <circle 
                        cx="50" cy="50" r={radius} 
                        className={`fill-none transition-all duration-1000 ease-out ${m2StrokeClass}`} 
                        strokeWidth="8"
                        strokeDasharray={circumference}
                        strokeDashoffset={m2StrokeDashoffset}
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center justify-center">
                      <span className={`text-2xl font-bold font-mono ${m2TextClass} ${isM2High ? 'neon-glow-red animate-pulse' : ''}`}>
                        {data.indice_desplazamiento.toFixed(0)}%
                      </span>
                      <span className="text-[8px] text-gray-500 uppercase tracking-widest">Fraude</span>
                    </div>
                  </div>

                  <div className="w-full text-center">
                    <span className="text-[10px] text-gray-400">Riesgo de irregularidad:</span>
                    <strong className={`ml-1 font-mono uppercase text-[10px] ${m2TextClass}`}>
                      {isM2High ? "Alto" : isM2Low ? "Bajo" : "Medio"}
                    </strong>
                  </div>
                </>
              )}
            </div>

            {/* Tarjeta 3: El Oráculo Urbano */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col justify-between min-h-[220px] shadow-lg shadow-black/50`}>
              <div className="w-full flex items-center justify-between text-xs font-semibold relative z-10">
                <span className="text-gray-400 uppercase tracking-wider flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-orange-400" /> Oráculo Urbano
                  <div className="relative group/tooltip">
                    <Info className="w-3.5 h-3.5 text-gray-500 hover:text-white cursor-pointer" />
                    <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-48 p-2 bg-black/95 border border-white/10 text-[10px] text-gray-300 rounded shadow-xl opacity-0 group-hover/tooltip:opacity-100 transition-opacity pointer-events-none z-50 normal-case tracking-normal">
                      Calculado mediante un Random Forest Regressor que pondera la probabilidad de especulación y la presión turística del barrio.
                    </div>
                  </div>
                </span>
                <span className="text-[10px] text-gray-500 font-mono">MÓDULO M3</span>
              </div>

              {loading ? (
                <div className="my-3 flex flex-col items-center justify-center space-y-4 flex-1">
                  <div className="w-24 h-10 bg-gray-800 animate-pulse rounded"></div>
                  <div className="w-32 h-4 bg-gray-800 animate-pulse rounded"></div>
                  <div className="w-full h-10 bg-gray-800 animate-pulse rounded mt-2"></div>
                </div>
              ) : (
                <>
                  <div className="my-3 text-center">
                    <div className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-amber-300 font-mono drop-shadow-[0_0_10px_rgba(251,146,60,0.6)]">
                      +{data.impacto_economico.toFixed(2)}
                      <span className="text-lg text-gray-400 ml-1 drop-shadow-none">€/m²</span>
                    </div>
                    <p className="text-[10px] text-gray-500 uppercase tracking-widest mt-1">Presión Inflacionaria</p>
                  </div>

                  <div className="text-[10px] leading-relaxed text-gray-400 border-t border-white/5 pt-3">
                    Este activo presiona al alza el alquiler de los vecinos de este barrio en un estimado de <strong className="text-orange-400 font-mono">+{(data.impacto_economico * 80).toFixed(0)}€</strong> al mes por cada vivienda de 80m².
                  </div>
                </>
              )}
            </div>

          </div>

          {/* MÓDULO CENTRAL INFERIOR: Consecuencias Sociales e Impacto */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Sección A: Criterio de Especulación */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col justify-between shadow-lg shadow-black/50`}>
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2 border-b border-white/5 pb-3">
                  <Coins className="w-4 h-4 text-orange-400" /> Ratio de Explotación Comercial
                </h3>
                
                {loading ? (
                  <div className="my-5 flex flex-col space-y-4">
                     <div className="w-full h-8 bg-gray-800 animate-pulse rounded"></div>
                     <div className="w-full h-8 bg-gray-800 animate-pulse rounded"></div>
                  </div>
                ) : (
                  <div className="my-5">
                    <div className="w-full bg-gray-800/80 rounded-full h-5 mb-3 overflow-hidden border border-white/5 shadow-inner relative">
                      <div 
                        className="bg-orange-500 h-full rounded-full absolute top-0 left-0 z-10 transition-all duration-1000 ease-out" 
                        style={{ width: `${Math.min(100, (data.detalles.ingreso_mensual_vut_estimado / Math.max(data.detalles.alquiler_residencial_estimado, data.detalles.ingreso_mensual_vut_estimado)) * 100)}%` }}
                      ></div> 
                      <div 
                        className="bg-emerald-500/80 h-full rounded-full absolute top-0 left-0 transition-all duration-1000 ease-out" 
                        style={{ width: `${Math.min(100, (data.detalles.alquiler_residencial_estimado / Math.max(data.detalles.alquiler_residencial_estimado, data.detalles.ingreso_mensual_vut_estimado)) * 100)}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-[10px] font-mono">
                      <span className="text-emerald-400 flex flex-col items-start">
                        <span>Residencial Medio</span>
                        <strong className="text-xs">{data.detalles.alquiler_residencial_estimado.toLocaleString('es-ES', {maximumFractionDigits: 0})} €</strong>
                      </span>
                      <span className="text-orange-400 flex flex-col items-end">
                        <span>Ingreso VUT Estimado</span>
                        <strong className="text-xs">{data.detalles.ingreso_mensual_vut_estimado.toLocaleString('es-ES', {maximumFractionDigits: 0})} €</strong>
                      </span>
                    </div>
                  </div>
                )}
              </div>

              <p className="text-xs text-gray-400 leading-relaxed bg-black/20 p-3.5 rounded-lg border border-white/5">
                Este inmueble genera <strong className="text-orange-400 font-mono">{loading ? "..." : `${data.ratio_explotacion_comercial} veces`}</strong> más ingresos operando como Vivienda de Uso Turístico (VUT) que si se alquilara a una familia de la localidad.
              </p>
            </div>

            {/* Sección B: Índice de Desplazamiento Comunitario */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col justify-between ${loading ? 'skeleton-shimmer' : ''}`}>
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2 border-b border-white/5 pb-3">
                  <Activity className="w-4 h-4 text-cyan-400" /> Índice de Desplazamiento Comunitario
                </h3>

                <div className="my-4 space-y-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-400">Suelo Bloqueado al Residente</span>
                    <span className="text-white font-mono">
                      {loading ? "..." : `${((365 - data.detalles.dias_ocupados_proyectados) / 365 * 100).toFixed(0)}% de los días`}
                    </span>
                  </div>
                  <div className="w-full bg-black/40 h-2 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-cyan-400 rounded-full transition-all duration-700"
                      style={{ width: `${loading ? 0 : ((365 - data.detalles.dias_ocupados_proyectados) / 365 * 100)}%` }}
                    />
                  </div>
                </div>
              </div>

              <div className="text-xs text-gray-400 leading-relaxed pt-2">
                Debido a la densidad turística de este entorno, se registra una <strong className="text-white">pérdida histórica del {data.eustat_poblacion_joven.toFixed(2)}%</strong> de población local joven en los últimos 5 años según el censo del Eustat. El pequeño comercio tradicional sufre un índice de desertización del <strong className="text-white">{data.eustat_desertizacion_comercio}%</strong>.
              </div>
            </div>

          </div>

          {/* Exportación Forense y Resumen */}
          <div className="flex justify-end gap-3 mt-2">
            <button 
              onClick={downloadForenseReport}
              className="bg-white/5 hover:bg-white/10 text-white border border-white/10 px-6 py-3 rounded-xl text-xs font-semibold tracking-wider uppercase transition-all flex items-center gap-2 hover:border-cyan-500/20"
            >
              <Download className="w-4 h-4 text-cyan-400" /> Descargar Reporte Forense (.JSON)
            </button>
          </div>

        </main>
      </div>

      {/* Pie de página */}
      <footer className="border-t border-white/5 py-4 px-6 text-center text-xs text-gray-600 bg-black/30 font-mono">
        © 2026 Especulómetro — Suite Predictiva de Especulometría. Licencia de Software Libre.
      </footer>

    </div>
  );
}
