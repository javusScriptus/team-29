import React, { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import '../styles/index.scss';
import type { AppProps } from 'next/app';
import { useRouter } from 'next/router';
import FontFaceObserver from 'fontfaceobserver';

import { GlobalStyles } from 'styles/GlobalStyles';
import { Layout } from 'components/Layout/Layout';

export default function MyApp(props: AppProps) {
  const { Component, pageProps } = props;
  const router = useRouter();

  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const fontA = new FontFaceObserver('opensans');

    Promise.all([fontA.load(null, 1000)])
      .then(
        () => {
          setIsReady(true);
        },
        () => {
          setIsReady(true);
          console.warn('Fonts were loading too long (over 2000ms)');
        },
      )
      .catch((err) => {
        setIsReady(true);
        console.warn('Some critical font are not available:', err);
      });
  }, []);

  return (
    <>
      <GlobalStyles />

      <AnimatePresence exitBeforeEnter={false}>
        <>
          <Layout isReady={isReady}>
            <Component
              key={router.route + router.locale}
              router={router}
              {...pageProps}
            />
          </Layout>
        </>
      </AnimatePresence>
    </>
  );
}
