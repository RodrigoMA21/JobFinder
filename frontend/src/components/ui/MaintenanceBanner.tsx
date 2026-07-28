import { useEffect, useState } from 'react';
import axios from 'axios';

export function MaintenanceBanner() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    axios
      .get('/api/v1/health', {
        signal: controller.signal,
        validateStatus: (status) => status === 503 || status === 200,
      })
      .then((res) => {
        if (res.status === 503) setShow(true);
      })
      .catch(() => {});
    return () => controller.abort();
  }, []);

  if (!show) return null;

  return (
    <div className="bg-amber-500 px-4 py-2 text-center text-sm font-medium text-white">
      O backend está temporariamente em manutenção. As vagas podem não carregar corretamente.
    </div>
  );
}
