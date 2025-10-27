// src/components/espaceAdmin/User.jsx
import React from 'react';
import SideBareAdmin from './SideBareAdmin';
import Header from '../Header';
import { useLocation } from 'react-router-dom';

const User = () => {
  const location = useLocation();
  const data = location.state;

  // Sécurité : vérifie que les données existent
  if (!data) {
    return (
      <div className='flex'>
        <SideBareAdmin />
        <div className='h-full w-full'>
          <Header />
          <div className='container mx-auto pt-11'>
            <p className='text-red-500'>Aucune donnée utilisateur trouvée.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className='flex'>
      <SideBareAdmin />
      <div className='h-full w-full'>
        <Header />
        <div className='container mx-auto flex flex-col gap-y-6 pt-11'>
          <div>
            <h2 className='text-2xl font-bold'>Nom complet :</h2>
            <p className='pl-6'>{data.name}</p> {/* full_name est envoyé comme "name" */}
          </div>
          <div>
            <h2 className='text-2xl font-bold'>Spécialité (Rôle) :</h2>
            <p className='pl-6'>{data.role}</p> {/* specialite → role */}
          </div>
          <div>
            <h2 className='text-2xl font-bold'>Email :</h2>
            <p className='pl-6'>{data.email}</p>
          </div>
          <div>
            <h2 className='text-2xl font-bold'>Compétences :</h2>
            <p className='pl-6'>{data.skills?.join(', ') || '—'}</p>
          </div>
          <div>
            <h2 className='text-2xl font-bold'>Charge de travail :</h2>
            <p className='pl-6'>{Math.round(data.workload * 100)}%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default User;