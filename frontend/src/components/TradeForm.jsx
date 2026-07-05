import { useState } from 'react'

const DIRECTIONS = ['buy', 'sell']
const RESULTS = ['pending', 'win', 'loss', 'breakeven']

const EMPTY_VALUES = {
  pair: '',
  direction: 'buy',
  entry_price: '',
  stop_loss: '',
  take_profit: '',
  risk_percent: '',
  result: 'pending',
  notes: '',
}

function toFormValues(initialValues) {
  if (!initialValues) return EMPTY_VALUES
  return {
    ...EMPTY_VALUES,
    ...initialValues,
    notes: initialValues.notes ?? '',
  }
}

const inputClasses =
  'w-full rounded-lg border border-slate-700 bg-slate-800/60 px-3 py-2 text-sm text-slate-100 outline-none focus:border-sky-500'
const labelClasses = 'mb-1 block text-xs font-medium uppercase tracking-wide text-slate-400'

export default function TradeForm({ initialValues, onSubmit, onCancel, submitting }) {
  const [values, setValues] = useState(() => toFormValues(initialValues))

  function update(field, value) {
    setValues((current) => ({ ...current, [field]: value }))
  }

  function handleSubmit(event) {
    event.preventDefault()
    onSubmit({
      pair: values.pair,
      direction: values.direction,
      entry_price: Number(values.entry_price),
      stop_loss: Number(values.stop_loss),
      take_profit: Number(values.take_profit),
      risk_percent: Number(values.risk_percent),
      result: values.result,
      notes: values.notes || null,
    })
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="grid gap-4 rounded-xl border border-slate-800 bg-slate-900/80 p-6 sm:grid-cols-2"
    >
      <div>
        <label className={labelClasses}>Pair</label>
        <input
          className={inputClasses}
          value={values.pair}
          onChange={(e) => update('pair', e.target.value)}
          placeholder="EURUSD"
          required
        />
      </div>

      <div>
        <label className={labelClasses}>Direction</label>
        <select
          className={inputClasses}
          value={values.direction}
          onChange={(e) => update('direction', e.target.value)}
        >
          {DIRECTIONS.map((direction) => (
            <option key={direction} value={direction}>
              {direction}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className={labelClasses}>Entry Price</label>
        <input
          className={inputClasses}
          type="number"
          step="any"
          value={values.entry_price}
          onChange={(e) => update('entry_price', e.target.value)}
          required
        />
      </div>

      <div>
        <label className={labelClasses}>Stop Loss</label>
        <input
          className={inputClasses}
          type="number"
          step="any"
          value={values.stop_loss}
          onChange={(e) => update('stop_loss', e.target.value)}
          required
        />
      </div>

      <div>
        <label className={labelClasses}>Take Profit</label>
        <input
          className={inputClasses}
          type="number"
          step="any"
          value={values.take_profit}
          onChange={(e) => update('take_profit', e.target.value)}
          required
        />
      </div>

      <div>
        <label className={labelClasses}>Risk %</label>
        <input
          className={inputClasses}
          type="number"
          step="any"
          min="0"
          max="100"
          value={values.risk_percent}
          onChange={(e) => update('risk_percent', e.target.value)}
          required
        />
      </div>

      <div>
        <label className={labelClasses}>Result</label>
        <select className={inputClasses} value={values.result} onChange={(e) => update('result', e.target.value)}>
          {RESULTS.map((result) => (
            <option key={result} value={result}>
              {result}
            </option>
          ))}
        </select>
      </div>

      <div className="sm:col-span-2">
        <label className={labelClasses}>Notes</label>
        <textarea
          className={inputClasses}
          rows={2}
          value={values.notes}
          onChange={(e) => update('notes', e.target.value)}
        />
      </div>

      <div className="flex items-center gap-3 sm:col-span-2">
        <button
          type="submit"
          disabled={submitting}
          className="rounded-lg bg-sky-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {submitting ? 'Saving…' : 'Save trade'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-slate-800"
        >
          Cancel
        </button>
      </div>
    </form>
  )
}
