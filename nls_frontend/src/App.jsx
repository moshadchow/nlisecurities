// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
import About from './pages/About'
import Contact from './pages/Contact'
import Service from './pages/Service'
import Director from './pages/Director'
import Home from './pages/Home'
import Feature from './pages/Feature'
import Header from './components/Header'
import Ipo from './pages/Ipo'
import Footer from './components/Footer'
import {Routes, Route} from 'react-router-dom'
import SimpleAreaChart from './pages/test';
import MarketNews from './pages/MarketNews';
import Branch from './pages/Branch';
import Sector from './pages/Sector';
import Download from './pages/Download';
import Event from './components/Event';
import ServiceDetails from './components/ServiceDetails';
import EventDetails from './components/EventDetails';
import PrivacyPolicy from './pages/PrivacyPolicy'
import ResearchPage from "./pages/ResearchPage";

function App() {
  return (
    <>    
    <Header/>    
    <Routes>
      <Route path='/' element={<Home/>}/>
      <Route path='/about' element={<About/>}/>
      <Route path='/service' element={<Service/>}/>
      <Route path='/director/' element={<Director/>}/>
      <Route path='/feature' element={<Feature/>}/>
      <Route path='/contact' element={<Contact/>}/>
      <Route path='/ipo' element={<Ipo/>}/>
      <Route path='/marketNews' element={<MarketNews/>}/>
      <Route path='/branch' element={<Branch/>}/>
      <Route path='/sector' element={<Sector/>}/>
      <Route path='/download' element={<Download/>}/>
      <Route path='/privacy-policy' element={<PrivacyPolicy/>}/>
      <Route path='/event/:id' element={<Event/>}/>
      <Route path='/service_dtl/:id' element={<ServiceDetails/>}/>
      <Route path='/event_dtl/:id' element={<EventDetails/>}/>
      <Route path="/research/:id" element={<ResearchPage />} />
      <Route path='/test' element={<SimpleAreaChart/>}/>
    </Routes>
    <Footer/>
    </>
  )
}

export default App
