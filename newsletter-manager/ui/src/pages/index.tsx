import classNames from "classnames";
import { type NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import { useRouter } from "next/router";
import React, { useState } from "react";
import { useSubscribe } from "../api/useSubscribe";
import { Button } from "../components/Button";
import { Input } from "../components/Input";
import { Label } from "../components/Label";
import { getReCaptchaProvider, getUseReCatpacha } from "../utils/useReCaptcha";

const ReCaptchaProvider = getReCaptchaProvider();
const useReCaptcha = getUseReCatpacha();

const Home = () => {
  const { isLoading, subscribe } = useSubscribe();
  const [form, setForm] = useState({ email: "" });
  const [error, setError] = useState("");
  const router = useRouter();

  const { executeRecaptcha } = useReCaptcha();

  async function handleSubscribe(e: React.FormEvent) {
    e.preventDefault();
    const token = await executeRecaptcha("subscribe");
    try {
      await subscribe({ email: form.email, token });
      await router.push("/success");
    } catch (err) {
      const error = err as Error;
      setError(error.message);
    }
  }

  return (
    <>
      <Head>
        <title>Subscribe | WebDevCody</title>
        <meta name="description" content="Generated by create-t3-app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="container m-auto mb-12 flex min-h-screen flex-col items-center gap-8 p-4 pt-20">
        <Image
          className="rounded-full"
          alt="web dev cody brand image"
          src="/wdc.jpeg"
          width="100"
          height="100"
        />
        <h1 className="text-center text-4xl font-bold">
          Subscribe to the
          <br /> WebDevCody Newsletter
        </h1>
        <p className="text-wdc-secondary max-w-screen-sm text-center text-xl">
          Subscribe to my newsletter and receive weekly updates on any community
          projects we are starting, recently published videos, and updates on
          new tutorials and courses.
        </p>

        {error && (
          <div className="rounded bg-red-200 p-2 text-black">{error}</div>
        )}

        <form
          onSubmit={(e) => {
            handleSubscribe(e).catch((err) => {
              console.error(err);
            });
          }}
          className="flex flex-col gap-6"
        >
          <fieldset className="flex flex-col gap-2">
            <Label htmlFor="email">Email</Label>
            <Input
              className={classNames("w-80")}
              placeholder="your-email@example.com"
              onChange={(e) => setForm({ email: e.currentTarget.value })}
              id="email"
              name="email"
              data-testid="email-input"
              required
              type="email"
            />
          </fieldset>
          <Button data-testid="subscribe-button" isLoading={isLoading}>
            {isLoading ? "Subscribing..." : "Subscribe"}
          </Button>
        </form>
      </main>
    </>
  );
};

const RecaptchWrapper: NextPage = () => {
  return (
    <ReCaptchaProvider>
      <Home />
    </ReCaptchaProvider>
  );
};

export default RecaptchWrapper;