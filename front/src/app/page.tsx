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
    informe_llm: "",
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
    "> Verificando sistemas institucionales...",
    "> Analizando Meta-Features en Módulo 3...",
    "> Calculando impacto territorial...",
    "> Redactando informe con Inteligencia Artificial (Qwen)..."
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


  // Cálculos dinámicos para el Donut Chart SVG
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (data.ratio_especulacion / 100) * circumference;

  const m1Ratio = data.ratio_especulacion;
  const isM1Red = m1Ratio > 66;
  const isM1Yellow = m1Ratio > 33 && m1Ratio <= 66;
  const isM1Green = m1Ratio <= 33;
  
  const m1StrokeClass = isM1Red ? 'stroke-red-600' : isM1Yellow ? 'stroke-yellow-500' : 'stroke-green-600';
  const m1GlowClass = isM1Red ? ' text-red-700' : isM1Yellow ? ' text-yellow-700' : ' text-green-700';
  const m1BorderClass = isM1Red ? 'border-red-300 bg-red-50' : isM1Yellow ? 'border-yellow-200 bg-yellow-50' : 'border-green-200 bg-green-50';

  return (
    <div className="min-h-screen text-gray-900 flex flex-col justify-between">
      
      {/* Cabecera Principal */}
      <header className="border-b border-gray-200 py-4 px-6 md:px-12 flex justify-between items-center bg-white/90 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="bg-blue-50 p-2 rounded-xl border border-blue-200">
            <Radar className="text-blue-700 w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-wider text-gray-900 flex items-center gap-2">
              ESPECULÓMETRO
            </h1>
          </div>
        </div>
      </header>

      {/* Buscador Principal (Tipo Google) */}
      <div className="w-full max-w-4xl mx-auto mt-8 px-4 flex-shrink-0 z-10">
        <form onSubmit={handleUrlAudit} className="relative shadow-sm rounded-full bg-white border border-gray-300 hover:shadow-md transition-shadow flex items-center p-2">
          <Search className="w-6 h-6 text-gray-400 ml-4 flex-shrink-0" />
          <input 
            type="text" 
            placeholder="Pegar URL de Airbnb o Booking para auditar..."
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            className="flex-1 bg-transparent border-none px-4 py-3 text-base text-gray-900 focus:outline-none focus:ring-0 placeholder:text-gray-400 w-full"
          />
          <button 
            type="submit" 
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-full px-8 py-3 text-sm transition-colors flex items-center justify-center disabled:opacity-50"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : "Auditar URL"}
          </button>
        </form>
        {errorMsg && <p className="text-xs text-red-600 mt-3 ml-6 font-medium">{errorMsg}</p>}
        {loading && activeTab === "url" && (
          <p className="text-sm text-blue-700 mt-3 ml-6 font-mono animate-pulse">
            {loadingTexts[loadingTextIndex]}
          </p>
        )}
      </div>

      {/* Main Container */}
      <div className="flex-1 flex flex-col lg:flex-row max-w-7xl w-full mx-auto p-4 md:p-8 gap-8 pt-4">
        
        {/* MÓDULO IZQUIERDO: Panel de Control (Sidebar) */}
        <aside className="rounded-2xl p-6 w-full lg:w-80 flex-shrink-0 flex flex-col gap-6 self-start lg:sticky lg:top-24 bg-white border border-gray-300 shadow-2xl shadow-sm backdrop-blur-xl z-40">
          
          <div className="border-b border-gray-200 pb-4">
            <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-widest">Control Manual</h2>
            <p className="text-xs text-gray-500 mt-1">Configura las variables para simular un escenario.</p>
          </div>

          {/* Manual sliders and selectors */}
          <div className={`space-y-6 ${activeTab === "url" ? "opacity-30 pointer-events-none" : ""}`}>
            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-600 flex items-center gap-2">
                <Map className="w-3.5 h-3.5 text-blue-700" /> Capital a Auditar
              </label>
              <select 
                value={municipio}
                onChange={(e) => setMunicipio(e.target.value)}
                className="w-full bg-white border border-gray-300 border border-gray-200 rounded-lg px-3 py-2.5 text-sm text-gray-900 focus:outline-none focus:border-blue-500 transition-colors"
              >
                <option value="Bilbao">Bilbao</option>
                <option value="San Sebastián">Donostia-San Sebastián</option>
                <option value="Vitoria-Gasteiz">Vitoria-Gasteiz</option>
              </select>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-gray-600 flex items-center gap-2">
                  <Coins className="w-3.5 h-3.5 text-orange-600" /> Tarifa por Noche
                </span>
                <span className="text-gray-900 font-mono">{precio} €</span>
              </div>
              <input 
                type="range" 
                min="30" 
                max="500" 
                value={precio}
                onChange={(e) => setPrecio(Number(e.target.value))}
                className="w-full accent-orange-600 h-1.5 bg-white border border-gray-300 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-[9px] text-gray-600 font-mono">
                <span>30€</span>
                <span>500€</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-gray-600 flex items-center gap-2">
                  <Building className="w-3.5 h-3.5 text-blue-700" /> Disponibilidad Anual
                </span>
                <span className="text-gray-900 font-mono">{disponibilidad} días</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="365" 
                value={disponibilidad}
                onChange={(e) => setDisponibilidad(Number(e.target.value))}
                className="w-full accent-blue-600 h-1.5 bg-white border border-gray-300 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-[9px] text-gray-600 font-mono">
                <span>0 días (Ocupado)</span>
                <span>365 días (Cartel)</span>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-600 flex items-center gap-2">
                <FileText className="w-3.5 h-3.5 text-blue-700" /> Descripción del Anuncio (NLP)
              </label>
              <textarea 
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Ej: Luxury flat managed by agency..."
                className="w-full bg-white border border-gray-300 border border-gray-200 rounded-lg px-3 py-2 text-xs text-gray-900 focus:outline-none focus:border-blue-500 transition-colors h-20 resize-none placeholder:text-gray-600"
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-600 flex items-center gap-2">
                <FileText className="w-3.5 h-3.5 text-blue-700" /> Perfil del Anfitrión (NLP)
              </label>
              <textarea 
                value={hostAbout}
                onChange={(e) => setHostAbout(e.target.value)}
                placeholder="Ej: We are an elite property team..."
                className="w-full bg-white border border-gray-300 border border-gray-200 rounded-lg px-3 py-2 text-xs text-gray-900 focus:outline-none focus:border-blue-500 transition-colors h-16 resize-none placeholder:text-gray-600"
              />
            </div>
          </div>

          {activeTab === "url" && (
            <button 
              onClick={handleReset}
              className="mt-2 w-full bg-gray-100 hover:bg-gray-200 text-gray-900 border border-gray-300 rounded-lg py-2.5 text-xs font-semibold transition-all flex items-center justify-center gap-2"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Volver a Control Manual
            </button>
          )}

        </aside>

        {/* CONTENEDOR CENTRAL: Módulos Superiores e Inferiores */}
        <main className="flex-1 flex flex-col gap-6">
          
          {/* Ficha del Alojamiento Scrapeado (si aplica) */}
          {activeTab === "url" && analyzedListing && (
            <div className="glass-panel rounded-2xl p-4 flex flex-col gap-4 border-blue-200 relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-blue-50 text-blue-700 border-l border-b border-blue-200 px-3 py-1 text-[10px] font-mono rounded-bl-lg uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="w-3 h-3 text-blue-700" /> Alojamiento Auditado
              </div>
              <div className="flex flex-col sm:flex-row gap-4">
                <img 
                  src={analyzedListing.image} 
                  alt="Airbnb" 
                  className="w-full sm:w-32 h-24 object-cover rounded-xl border border-gray-200 flex-shrink-0"
                />
                <div className="flex-1 flex flex-col justify-between py-1">
                  <div>
                    <h3 className="text-base font-bold text-gray-900 leading-tight mb-1">{analyzedListing.title}</h3>
                    <p className="text-xs text-gray-600 flex items-center gap-1.5">
                      <Map className="w-3 h-3 text-blue-700" /> {analyzedListing.municipio}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-4 text-xs font-mono mt-3 sm:mt-0">
                    <span className="text-gray-600">Anfitrión: <strong className="text-gray-900">{analyzedListing.host_name}</strong></span>
                    <span className="text-gray-300">|</span>
                    <span className="text-gray-600">Cartera: <strong className="text-blue-700">{analyzedListing.host_listings_count} anuncios</strong></span>
                    <span className="text-gray-300">|</span>
                    <span className="text-gray-600">Tarifa: <strong className="text-gray-900">{analyzedListing.price}€/noche</strong></span>
                    <span className="text-gray-300">|</span>
                    <span className="text-gray-600">Oferta: <strong className="text-gray-900">{analyzedListing.availability}d/año</strong></span>
                  </div>
                </div>
              </div>

              {/* Desplegable de NLP Scrapeado */}
              {analyzedListing.description_scraped && (
                <details className="mt-2 border border-gray-200 rounded-lg group">
                  <summary className="text-xs font-semibold text-gray-700 cursor-pointer p-3 bg-gray-50 hover:bg-gray-100 rounded-lg flex items-center gap-2 list-none select-none">
                    <FileText className="w-4 h-4 text-blue-600" /> 
                    <span>Ver Texto Base Scrapeado para NLP</span>
                    <span className="ml-auto transform group-open:rotate-90 transition-transform">
                      <ArrowRight className="w-4 h-4 text-gray-400" />
                    </span>
                  </summary>
                  <div className="p-4 border-t border-gray-200 bg-white">
                    <p className="text-[10px] font-mono text-gray-600 whitespace-pre-wrap max-h-48 overflow-y-auto">
                      {analyzedListing.description_scraped}
                    </p>
                  </div>
                </details>
              )}
            </div>
          )}

          {/* MÓDULO CENTRAL SUPERIOR: El Panel Unimodular (Métricas de la IA) */}
          <div className="grid grid-cols-1 max-w-md mx-auto w-full gap-6">
            
            {/* Tarjeta 1: El Especulómetro */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col items-center justify-between min-h-[220px] shadow-lg shadow-sm transition-all relative group ${!loading ? m1BorderClass : ''}`}>
              <div className="w-full flex items-center justify-between text-xs font-semibold relative z-10">
                <span className="text-gray-600 uppercase tracking-wider flex items-center gap-2">
                  <AlertTriangle className={`w-4 h-4 ${!loading ? (isM1Red ? 'text-red-700' : isM1Yellow ? 'text-yellow-700' : 'text-green-700') : 'text-gray-500'}`} /> Especulómetro
                  <div className="relative group/tooltip">
                    <Info className="w-3.5 h-3.5 text-gray-500 hover:text-gray-900 cursor-pointer" />
                    <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-48 p-2 bg-white border border-gray-300 text-[10px] text-gray-700 rounded shadow-xl opacity-0 group-hover/tooltip:opacity-100 transition-opacity pointer-events-none z-50 normal-case tracking-normal">
                      Identifica si el propietario opera múltiples pisos (gran tenedor) actuando como una empresa bajo el radar.
                    </div>
                  </div>
                </span>
                <span className="text-[10px] text-gray-500 font-mono">MÓDULO M1</span>
              </div>
              
              {loading ? (
                <div className="flex flex-col items-center justify-center my-3 w-full space-y-4">
                  <div className="w-24 h-24 rounded-full bg-gray-100 animate-pulse border-[8px] border-gray-700/50"></div>
                  <div className="w-3/4 h-6 bg-gray-100 animate-pulse rounded"></div>
                </div>
              ) : (
                <>
                  {/* Donut Chart SVG */}
                  <div className="relative w-28 h-28 flex items-center justify-center my-3">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle 
                        cx="50" cy="50" r={radius} 
                        className="stroke-gray-200 fill-none" 
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
                      <span className="text-[10px] font-bold text-red-700 bg-red-100 px-2.5 py-1 rounded border border-red-200 block animate-pulse">
                        Alerta: Explotación Profesional/Multi-host
                      </span>
                    ) : isM1Yellow ? (
                      <span className="text-[10px] font-bold text-yellow-700 bg-yellow-100 px-2.5 py-1 rounded border border-yellow-200 block">
                        Aviso: Actividad Comercial Moderada
                      </span>
                    ) : (
                      <span className="text-[10px] text-green-700 bg-green-100 px-2.5 py-1 rounded border border-green-200 block">
                        Particular / Operación moderada
                      </span>
                    )}
                  </div>
                </>
              )}
            </div>

          </div>

          {/* MÓDULO CENTRAL INFERIOR: Consecuencias Sociales e Impacto */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Sección A: Criterio de Especulación */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col justify-between shadow-lg shadow-sm`}>
              <div>
                <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2 border-b border-gray-200 pb-3">
                  <Coins className="w-4 h-4 text-orange-700" /> Ratio de Explotación Comercial
                </h3>
                
                {loading ? (
                  <div className="my-5 flex flex-col space-y-4">
                     <div className="w-full h-8 bg-gray-100 animate-pulse rounded"></div>
                     <div className="w-full h-8 bg-gray-100 animate-pulse rounded"></div>
                  </div>
                ) : (
                  <div className="my-5">
                    <div className="w-full bg-gray-200 rounded-full h-5 mb-3 overflow-hidden border border-gray-200 shadow-inner relative">
                      <div 
                        className="bg-orange-600 h-full rounded-full absolute top-0 left-0 z-10 transition-all duration-1000 ease-out" 
                        style={{ width: `${Math.min(100, (data.detalles.ingreso_mensual_vut_estimado / Math.max(data.detalles.alquiler_residencial_estimado, data.detalles.ingreso_mensual_vut_estimado)) * 100)}%` }}
                      ></div> 
                      <div 
                        className="bg-green-600 h-full rounded-full absolute top-0 left-0 transition-all duration-1000 ease-out" 
                        style={{ width: `${Math.min(100, (data.detalles.alquiler_residencial_estimado / Math.max(data.detalles.alquiler_residencial_estimado, data.detalles.ingreso_mensual_vut_estimado)) * 100)}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-[10px] font-mono">
                      <span className="text-green-700 flex flex-col items-start">
                        <span>Residencial Medio</span>
                        <strong className="text-xs">{data.detalles.alquiler_residencial_estimado.toLocaleString('es-ES', {maximumFractionDigits: 0})} €</strong>
                      </span>
                      <span className="text-orange-700 flex flex-col items-end">
                        <span>Ingreso VUT Estimado</span>
                        <strong className="text-xs">{data.detalles.ingreso_mensual_vut_estimado.toLocaleString('es-ES', {maximumFractionDigits: 0})} €</strong>
                      </span>
                    </div>
                  </div>
                )}
              </div>

              <p className="text-xs text-gray-600 leading-relaxed bg-gray-50 p-3.5 rounded-lg border border-gray-200">
                Este inmueble genera <strong className="text-orange-700 font-mono">{loading ? "..." : `${data.ratio_explotacion_comercial} veces`}</strong> más ingresos operando como Vivienda de Uso Turístico (VUT) que si se alquilara a una familia de la localidad.
              </p>
            </div>

            {/* Sección B: Índice de Desplazamiento Comunitario */}
            <div className={`glass-panel rounded-2xl p-6 flex flex-col justify-between ${loading ? 'skeleton-shimmer' : ''}`}>
              <div>
                <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2 border-b border-gray-200 pb-3">
                  <Activity className="w-4 h-4 text-blue-700" /> Índice de Desplazamiento Comunitario
                </h3>

                <div className="my-4 space-y-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-600">Suelo Bloqueado al Residente</span>
                    <span className="text-gray-900 font-mono">
                      {loading ? "..." : `${((365 - data.detalles.dias_ocupados_proyectados) / 365 * 100).toFixed(0)}% de los días`}
                    </span>
                  </div>
                  <div className="w-full bg-white border border-gray-300 h-2 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-cyan-400 rounded-full transition-all duration-700"
                      style={{ width: `${loading ? 0 : ((365 - data.detalles.dias_ocupados_proyectados) / 365 * 100)}%` }}
                    />
                  </div>
                </div>
              </div>

              <div className="text-xs text-gray-600 leading-relaxed pt-2">
                Debido a la densidad turística de este entorno, se registra una <strong className="text-gray-900">pérdida histórica del {data.eustat_poblacion_joven.toFixed(2)}%</strong> de población local joven en los últimos 5 años según el censo del Eustat. El pequeño comercio tradicional sufre un índice de desertización del <strong className="text-gray-900">{data.eustat_desertizacion_comercio}%</strong>.
              </div>
            </div>

          </div>

          {/* Informe Narrativo IA */}
          {data.informe_llm && (
            <div className="mt-4 glass-panel rounded-2xl p-6 shadow-lg shadow-sm border border-blue-200/50 relative overflow-hidden bg-gradient-to-r from-blue-50/50 to-white">
              <div className="absolute top-0 right-0 bg-blue-100 text-blue-800 px-3 py-1 text-[10px] font-mono rounded-bl-lg uppercase tracking-wider flex items-center gap-1.5 border-b border-l border-blue-200">
                <Activity className="w-3 h-3 text-blue-700 animate-pulse" /> Qwen2.5-0.5B AI
              </div>
              <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2 mb-3">
                <FileText className="w-4 h-4 text-blue-700" /> Diagnóstico Ejecutivo Automático
              </h3>
              <p className="text-sm text-gray-700 leading-relaxed italic border-l-2 border-blue-400 pl-4 bg-white/50 p-3 rounded-r">
                "{data.informe_llm}"
              </p>
            </div>
          )}

        </main>
      </div>

      {/* Pie de página */}
      <footer className="border-t border-gray-200 py-4 px-6 text-center text-xs text-gray-600 bg-white font-mono">
        © 2026 Especulómetro — Sistema de Inteligencia Territorial.
      </footer>

    </div>
  );
}
